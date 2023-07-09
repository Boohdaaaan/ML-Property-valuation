from aiogram import executor

from create_bot import dp
from handlers import user


async def on_startup(_):
    print('Go!')


user.register_handler_user(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
