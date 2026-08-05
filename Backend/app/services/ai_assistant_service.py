import httpx
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class AIAssistantService:
    """
    Multi-provider LLM service with automatic failover.

    Provider priority order (first available wins):
      1. Ollama Cloud  — ollama.com hosted models (DEFAULT, requires API key)
      2. Ollama Local  — self-hosted on localhost (no API key needed)
      3. Groq          — free tier, fast inference
      4. Gemini        — Google free tier
      5. HuggingFace   — free tier
      6. OpenAI        — paid
      7. Anthropic     — paid

    Enable providers in Backend/.env — see comments there for instructions.
    """

    def __init__(self):
        self.providers = []

        # ── 1. Ollama Cloud (DEFAULT) ─────────────────────────────────────────
        if settings.OLLAMA_CLOUD_ENABLED and settings.OLLAMA_API_KEY:
            self.providers.append(self._call_ollama_cloud)

        # ── 2. Ollama Local (fallback) ────────────────────────────────────────
        if settings.OLLAMA_ENABLED:
            self.providers.append(self._call_ollama_local)

        # ── 3-7. Other cloud providers ────────────────────────────────────────
        if settings.GROQ_API_KEY:
            self.providers.append(self._call_groq)
        if settings.GEMINI_API_KEY:
            self.providers.append(self._call_gemini)
        if settings.HF_API_KEY:
            self.providers.append(self._call_huggingface)
        if settings.OPENROUTER_API_KEY:
            self.providers.append(self._call_openrouter)
        if settings.OPENAI_API_KEY:
            self.providers.append(self._call_openai)
        if settings.ANTHROPIC_API_KEY:
            self.providers.append(self._call_anthropic)

    async def generate_response(self, context_str: str, user_message: str, history: list = None) -> str:
        """Attempt each configured provider in order until one succeeds."""
        if not self.providers:
            return (
                "No AI provider is configured. "
                "Add an API key or enable Ollama in Backend/.env to use the assistant."
            )

        if history is None:
            history = []

        system_prompt = (
            "You are FinWise AI, a helpful, encouraging, and highly intelligent personal finance assistant. "
            "Speak directly to the user, provide concise, practical advice, and never output raw JSON."
        )

        augmented_user_message = f"USER FINANCIAL CONTEXT:\n{context_str}\n\nUSER MESSAGE:\n{user_message}"

        messages = [{"role": "system", "content": system_prompt}]
        for h in history:
            messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
        messages.append({"role": "user", "content": augmented_user_message})

        last_error = ""
        for provider_func in self.providers:
            try:
                response = await provider_func(messages)
                if response:
                    return response
            except Exception as e:
                logger.warning(f"AI Provider {provider_func.__name__} failed: {e}")
                last_error = str(e)
                continue

        if "429" in last_error and "openai.com" in last_error:
            return "Your OpenAI API key has hit its rate limit or run out of credits. Please check your billing dashboard or configure a different free provider (like Groq, Gemini, or OpenRouter) in the Backend/.env file."
        elif "401" in last_error or "400" in last_error:
            return f"API Authentication failed. Please ensure your API keys in Backend/.env are valid. (Details: {last_error})"

        return (
            "I'm temporarily unable to process your request. "
            f"Please try again in a few moments. (Error: {last_error})"
        )

    # ── Ollama Cloud ──────────────────────────────────────────────────────────
    async def _call_ollama_cloud(self, messages: list) -> Optional[str]:
        url = "https://ollama.com/api/chat"
        payload = {
            "model": settings.OLLAMA_CLOUD_MODEL,
            "messages": messages,
            "stream": False,
        }
        headers = {
            "Authorization": f"Bearer {settings.OLLAMA_API_KEY}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code != 200:
                logger.error(f"Ollama Cloud error {resp.status_code}: {resp.text}")
            resp.raise_for_status()
            return resp.json()["message"]["content"]

    # ── Ollama Local ──────────────────────────────────────────────────────────
    async def _call_ollama_local(self, messages: list) -> Optional[str]:
        url = f"{settings.OLLAMA_HOST}/api/chat"
        payload = {
            "model": settings.OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code != 200:
                logger.error(f"Ollama Local error {resp.status_code}: {resp.text}")
            resp.raise_for_status()
            return resp.json()["message"]["content"]

    # ── Free-tier cloud providers ─────────────────────────────────────────────
    async def _call_groq(self, messages: list) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "max_tokens": 1024,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers, json=payload,
            )
            if resp.status_code != 200:
                logger.error(f"Groq API Error: {resp.text}")
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    async def _call_gemini(self, messages: list) -> Optional[str]:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"
        )
        system = messages[0]["content"] if messages[0]["role"] == "system" else ""
        contents = []
        for m in messages:
            if m["role"] == "system": continue
            role = "user" if m["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": m["content"]}]})
        if system and contents:
            contents[0]["parts"][0]["text"] = f"System: {system}\n\n{contents[0]['parts'][0]['text']}"

        payload = {"contents": contents}
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

    async def _call_huggingface(self, messages: list) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {settings.HF_API_KEY}",
            "Content-Type": "application/json",
        }
        prompt = ""
        for m in messages:
            prompt += f"{m['role'].upper()}: {m['content']}\n\n"
        prompt += "ASSISTANT:"
        
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 512, "return_full_text": False},
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                headers=headers, json=payload,
            )
            resp.raise_for_status()
            result = resp.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
            return None

    # ── Paid cloud providers ──────────────────────────────────────────────────
    async def _call_openrouter(self, messages: list) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "FinWise",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "google/gemini-2.0-flash-lite-preview-02-05:free",
            "messages": messages,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers, json=payload,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    async def _call_openai(self, messages: list) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers, json=payload,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    async def _call_anthropic(self, messages: list) -> Optional[str]:
        headers = {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        system = messages[0]["content"] if messages[0]["role"] == "system" else ""
        user_msgs = [m for m in messages if m["role"] != "system"]
        payload = {
            "model": "claude-3-haiku-20240307",
            "system": system,
            "messages": user_msgs,
            "max_tokens": 1024,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers, json=payload,
            )
            resp.raise_for_status()
            return resp.json()["content"][0]["text"]

ai_assistant_service = AIAssistantService()
