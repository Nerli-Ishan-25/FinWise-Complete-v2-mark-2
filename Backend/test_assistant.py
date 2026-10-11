import asyncio
import logging
import sys
from app.services.ai_assistant_service import ai_assistant_service

logging.basicConfig(level=logging.WARNING, stream=sys.stdout)

async def test():
    Result = await ai_assistant_service.generate_response("Context", "Hello")
    print("\nFINAL RESULT:", Result)

asyncio.run(test())
