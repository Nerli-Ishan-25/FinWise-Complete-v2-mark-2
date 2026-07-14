import urllib.request
import json
import os

url = "http://localhost:11434/api/chat"
payload = {
    "model": "gemma4:31b-cloud",
    "messages": [
        {"role": "system", "content": "hello"},
        {"role": "user", "content": "hi"}
    ],
    "stream": False
}
req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except Exception as e:
    print("Error:", e)
