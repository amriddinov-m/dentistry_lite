import os
import sys
import logging
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# os.environ['DJANGO_SETTINGS_MODULE'] = 'garbus.settings'
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# import django
#
# django.setup()

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token='5572492160:AAEL_pd6CsZ5ZSo2rAUkOWX9H-iTo8wamV4')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


__all__ = ['bot', 'loader', 'dp']