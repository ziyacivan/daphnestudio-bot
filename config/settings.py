import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GUILD_ID = int(os.environ.get("GUILD_ID", 0))  # Add your server ID to .env file
AUTO_ROLE_ID = 1456815542148137030
EMBED_CREATOR_ROLES = [1456378940620017779, 1456755943952875735]
