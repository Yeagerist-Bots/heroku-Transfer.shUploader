from decouple import config
import redis

APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
CHANNEL = config("CHANNEL", default=None)
REDIS_URI = config("REDIS_URI", default=None)
REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
