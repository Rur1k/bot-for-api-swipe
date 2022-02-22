import keyboard
import datetime

from aiogram import types
from aiogram import executor
from load_all import bot, dp, sqlite_db
from peewee import *
from request_api import login

login()
