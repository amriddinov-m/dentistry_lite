import os
import django
from bot.set_bot_commands import set_default_commands


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "dentistry_light.settings"
    )
    os.environ.setdefault(
        'DJANGO_ALLOW_ASYNC_UNSAFE',
        'true'
    )
    django.setup()


async def on_startup(dispatcher):
    """Устанавливаем дефолтные команды"""
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    setup_django()

    from aiogram.utils import executor
    from bot.handler import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
