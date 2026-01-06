import discord
from clients.bot_client import BotClient
from config import settings


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = BotClient(intents=intents)
client.run(settings.BOT_TOKEN)
