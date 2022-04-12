import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
que = {}

BOT_USERNAME = getenv("BOT_USERNAME")
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "MissMuzikAsistan")
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

HEROKU_API_KEY = getenv("HEROKU_API_KEY")
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))

COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ !").split())

SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
