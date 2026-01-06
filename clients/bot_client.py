import discord
from discord.ext import commands
from config import settings


class BotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        await self.load_extension("commands.embed_commands")

        # Sync commands to guild for instant updates
        if settings.GUILD_ID:
            guild = discord.Object(id=settings.GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"Synced commands to guild {settings.GUILD_ID}")
        else:
            await self.tree.sync()
            print("Synced commands globally")

    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_member_join(self, member):
        role = member.guild.get_role(settings.AUTO_ROLE_ID)

        if role:
            try:
                await member.add_roles(role)
                print(f"Assigned role {role.name} to {member.display_name}")
            except discord.Forbidden:
                print(
                    f"Error: No permission to assign role {role.name} to {member.display_name}"
                )
        else:
            print(
                f"Error: Role with ID {settings.AUTO_ROLE_ID} not found in guild {member.guild.name}"
            )
