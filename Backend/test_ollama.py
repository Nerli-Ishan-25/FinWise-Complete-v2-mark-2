import asyncio
import httpx
import logging
import sys

logging.basicConfig(level=logging.WARNING, stream=sys.stdout)

async def test_ollama():
    url = "https://ollama.com/api/chat"
    payload = {
        "model": "gpt-oss:120b-cloud",
        "messages": [
            {"role": "system", "content": "hi"},
            {"role": "user",   "content": "hello"},
        ],
        "stream": False,
    }
    headers = {
        "Authorization": "Bearer 3815dc7434814c55a3b5da7873a8ccc1.QEvHRZrhXxR1IaLNnr7dQ6M9",
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            print("Status:", resp.status_code)
            print("Text:", resp.text)
            resp.raise_for_status()
    except Exception as e:
        print("EXCEPTION TYPE:", type(e))
        print("EXCEPTION ARGS:", e.args)

asyncio.run(test_ollama())
