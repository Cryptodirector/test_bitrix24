import os
import aiohttp
from dotenv import load_dotenv
from sqlalchemy import select
from src.app.models import Man, Woman
from src.database.config import async_session_maker

load_dotenv()

TOKEN = os.getenv('TOKEN')


class Service:

    # Получаем информацию о пользователе
    @staticmethod
    async def get_info_user():

        url = f'https://b24-7ltyoa.bitrix24.ru/rest/1/{TOKEN}/user.current.json'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 401:
                    print(
                        {
                            'status': response.status,
                            'detail': 'Неверный токен'
                        }
                    )
                profile = await response.json()
                return profile

    # Проверяем в таблице man, если пользователь с таким именем
    @staticmethod
    async def check_name_man_in_db():
        name = await Service.get_info_user()
        async with async_session_maker() as session:
            query = select(Man.name).where(Man.name == name['result']['NAME'])
            result = await session.execute(query)

            if result.scalar() == name['result']['NAME']:
                return True
            else:
                return False

    # Проверяем в таблице woman, если пользователь с таким именем
    @staticmethod
    async def check_name_woman_in_db():
        name = await Service.get_info_user()
        async with async_session_maker() as session:
            query = select(Woman.name).where(Woman.name == name['result']['NAME'])
            result = await session.execute(query)

            if result.scalar() == name['result']['NAME']:
                return True

            else:
                return False

    # Если пользователь с таким именем есть, передаем данные по гендеру обратно в контакт по ID

    @staticmethod
    async def insert_info():
        id = await Service.get_info_user()
        gender = ''
        async with aiohttp.ClientSession() as session:
            if await Service.check_name_man_in_db() is True:
                gender = 'Мужской'

            elif await Service.check_name_woman_in_db() is True:
                gender = 'Женский'

            async with session.patch(
                    f'https://b24-7ltyoa.bitrix24.ru/rest/1/'
                    f'{TOKEN}/user.update.json?ID={id["result"]["ID"]}&PERSONAL_GENDER={gender}'
            ) as response:
                if response.status == 401:
                    print(
                        {
                            'status': response.status,
                            'detail': 'Неверный токен'
                        }
                    )
                elif response.status == 500:
                    print(
                        {
                            'status': response.status,
                            'detail': 'серверная ошибка'
                        }
                    )
                return {'status': 'OK', 'gender': gender}


service = Service()
