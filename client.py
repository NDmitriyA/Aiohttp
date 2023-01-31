import asyncio
from aiohttp import ClientSession


async def check_status():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:7070/status') as resp:
            return await resp.json()


async def get_advertisements():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:7070/admodels') as resp:
            return await resp.text()


async def get_advertisement():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:7070/admodel/1') as resp:
            return await resp.text()


async def create_advertisement():
    async with ClientSession() as session:
        async with session.post('http://127.0.0.1:7070/admodel', json={
            "title": "Selling an aquarium fish",
            "description": "Guppi fish, really cute",
            "created_at": "26.01.2023",
            "owner": "Drin Nik"

        }) as resp:
            return await resp.text()


async def delete_advertisement():
    async with ClientSession() as session:
        async with session.delete('http://127.0.0.1:7070/admodel/2') as resp:
            return await resp.text()


async def main():
    response = await check_status()
    print(response)
    response = await create_advertisement()
    print(response)
    response = await get_advertisements()
    print(response)
    response = await get_advertisement()
    print(response)

    response = await delete_advertisement()
    print(response)


asyncio.run(main())

