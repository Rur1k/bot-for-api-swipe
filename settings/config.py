import os
import sys

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
API = os.getenv("API")
AUTH = os.getenv("AUTH")
