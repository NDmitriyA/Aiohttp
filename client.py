import asyncio
from aiohttp import ClientSession


async def check_status():
    async with ClientSession() as session:
        async with session.get(f'http://127.0.0.1:7070/status') as resp:
            return await resp.json()


async def create_advertisement():
    async with ClientSession() as session:
        async with session.post(f'http://127.0.0.1:7070/admodel', json={

            "title": "Selling an aquarium fish",
            "description": "Guppi fish, really cute",
            "created_at": "26.01.2023",
            "owner": "Drin Nik"

        }) as resp:
            if resp.status != 201:
                return await resp.text()
            return await resp.json()


async def get_advertisements():
    async with ClientSession() as session:
        async with session.get(f'http://127.0.0.1:7070/admodels') as resp:
            return await resp.json()


async def get_advertisement():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:7070/admodel/') as resp:
            return await resp.text()


async def delete_advertisement():
    async with ClientSession() as session:
        async with session.delete('http://127.0.0.1:7070/admodel/1') as resp:
            return {"status": resp.status}


async def main():
    response = await check_status()
    print(response)
    response1 = await create_advertisement()
    print(response1)
    response2 = await get_advertisements()
    print(response2)
    response3 = await get_advertisement()
    print(response3)

    response4 = await delete_advertisement()
    print(response4)


asyncio.run(main())
