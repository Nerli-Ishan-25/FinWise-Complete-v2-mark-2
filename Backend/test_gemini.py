import asyncio
import httpx
import os

async def test_gemini():
    keys = [
        "AIzaSyA-2fjnXma5osX6uGFYwRYTdMGAakCAN-Y", # From .env
        "AIzaSyA_6fU9jjKQGOC67dEk-ilgQt5pwHoArQE"  # From Env Vars
    ]
    models = ["gemini-1.5-flash", "gemini-2.0-flash"]
    
    for key in keys:
        for model in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            payload = {"contents": [{"role": "user", "parts": [{"text": "Hello"}]}]}
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    resp = await client.post(url, json=payload)
                    print(f"Key: {key[:10]}... Model: {model} Status: {resp.status_code}")
                    if resp.status_code == 200:
                        print(resp.json()["candidates"][0]["content"]["parts"][0]["text"])
            except Exception as e:
                print(f"Error for {model} with key {key[:10]}...: {e}")

asyncio.run(test_gemini())
