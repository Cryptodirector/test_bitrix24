import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
from models import Man, Woman
from src.database.config import async_session_maker
from sqlalchemy import insert


class Parser:

    # Парсим с сайта все имена мужские/женские

    @staticmethod
    async def get_name(gender: str):
        async with aiohttp.ClientSession() as session:
            name = []
            for page in range(1, 6):
                async with session.get(
                        f'https://deti.mail.ru/names/{gender}/slavyanskoe/?page={page}'  # male/female
                ) as response:

                    soup = bs(await response.text(), 'html.parser')
                    card = soup.find('ul', {'class': 'list deti-name__items'}) \
                        .find_all('span', {'class': 'link__text'})
                    for names in card:
                        name.append(names.text)
            return name

    # Добавляем в бд имена

    @staticmethod
    async def insert_to_db():
        lst_name = await Parser.get_name('male')  # male/female

        async with async_session_maker() as session:
            for name in lst_name:
                stmt = insert(Man).values(name=name)
                await session.execute(stmt)

            await session.commit()


asyncio.run(Parser.insert_to_db())
