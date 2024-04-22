import asyncio

from src.app.service import service


async def main():
    await service.insert_info()


if __name__ == '__main__':
    asyncio.run(main())

