import asyncio
import edge_tts

async def list_voices():
    voices = await edge_tts.list_voices()
    for voice in voices:
        if "IN" in voice["ShortName"]:
            print(f"{voice['ShortName']} ({voice['Locale']})")

if __name__ == "__main__":
    asyncio.run(list_voices())
