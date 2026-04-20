import httpx
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class AIAssistantService:
    """
    Multi-provider LLM service with automatic failover.

    Provider priority (configurable via .env):
      Free  → Groq, Gemini, HuggingFace
      Paid  → OpenAI, Anthropic

    Only providers whose API key is set in .env are activated.
    """

    def __init__(self):
        self.providers = []
        if settings.GROQ_API_KEY:
            self.providers.append(self._call_groq)
        if settings.GEMINI_API_KEY:
            self.providers.append(self._call_gemini)
        if settings.HF_API_KEY:
            self.providers.append(self._call_huggingface)
        if settings.OPENAI_API_KEY:
            self.providers.append(self._call_openai)
        if settings.ANTHROPIC_API_KEY:
            self.providers.append(self._call_anthropic)

    async def generate_response(self, context_str: str, user_message: str) -> str:
        """Attempt each configured provider in order until one succeeds."""
        if not self.providers:
            return "Server configuration error: No AI providers configured."

        system_prompt = (
            "You are FinWise AI, a helpful, encouraging, and highly intelligent personal finance assistant. "
            "You have access to the user's current financial profile. Speak directly to them, provide concise, "
            "practical advice, and never output raw JSON. If they ask about their finances, use the context below.\n\n"
            f"USER CONTEXT:\n{context_str}"
        )

        last_error = ""
        for provider_func in self.providers:
            try:
                response = await provider_func(system_prompt, user_message)
                if response:
                    return response
            except Exception as e:
                logger.warning(f"AI Provider {provider_func.__name__} failed: {e}")
                last_error = str(e)
                continue

        return (
            "I'm temporarily unable to process your request. "
            f"Please try again in a few moments. (Error: {last_error})"
        )

    # ── Free-tier providers ───────────────────────────────────────────────

    async def _call_groq(self, system_prompt: str, user_message: str) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": 1024,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers, json=payload,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    async def _call_gemini(self, system_prompt: str, user_message: str) -> Optional[str]:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={settings.GEMINI_API_KEY}"
        )
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": f"{system_prompt}\n\nUser: {user_message}"}],
            }],
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

    async def _call_huggingface(self, system_prompt: str, user_message: str) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {settings.HF_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "inputs": f"{system_prompt}\n\nUser: {user_message}\nFinWise AI:",
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

    # ── Paid providers ────────────────────────────────────────────────────

    async def _call_openai(self, system_prompt: str, user_message: str) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers, json=payload,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    async def _call_anthropic(self, system_prompt: str, user_message: str) -> Optional[str]:
        headers = {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "claude-3-haiku-20240307",
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_message}],
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
