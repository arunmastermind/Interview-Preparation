import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay)
    return f"{name} complete"

async def main():
    results = await asyncio.gather(
        fetch("model-a", 1),
        fetch("model-b", 1),
        fetch("model-c", 1),
    )
    print(results)

asyncio.run(main())