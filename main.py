import asyncio

from src.app.service import service


async def main():
    await service.get_info_user()


if __name__ == '__main__':
    asyncio.run(main())

