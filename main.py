from dotenv import load_dotenv

load_dotenv()
import os
from discord_role_expire import db
from discord_role_expire.bot import bot

db.init()

bot.run(os.getenv("TOKEN"))
