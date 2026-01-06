import discord
from discord import app_commands
from discord.ext import commands
from ui.views import LinksView, RulesView, EmbedCreationView
from config import settings


class EmbedCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="links", description="View important Daphne Studio links"
    )
    @app_commands.checks.has_any_role(*settings.EMBED_CREATOR_ROLES)
    async def links(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=LinksView())

    @app_commands.command(name="rules", description="View server rules")
    @app_commands.checks.has_any_role(*settings.EMBED_CREATOR_ROLES)
    async def rules(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Daphne Studio - Server Rules",
            description="Click the **I have read and accept the rules.** button below to get access to the server.",
            color=discord.Color.dark_grey(),
        )

        embed.add_field(
            name="Discord Rules",
            value="Follow Discord's Terms of Service and Community Guidelines.\n[Terms of Service](https://discord.com/terms) | [Community Guidelines](https://discordapp.com/guidelines)",
            inline=False,
        )

        embed.add_field(
            name="STICK",
            value="📕 **English-Only Chat**\nThis is an international community; please keep all conversations and questions in English. Using a translator is fine.\n\n📕 **Avoid Spam & Toxicity**\nSpamming, aggressive behavior, or toxic discussions will not be tolerated.\n\n📕 **Impersonation**\nImpersonating other users, bots, or public figures is strictly prohibited.",
            inline=True,
        )

        embed.add_field(
            name="TO THE",
            value="📙 **Respect & Maturity**\nMaintain a respectful and mature tone in all conversations. No excessive profanity, hate speech, harassment, or personal attacks. Do not randomly tag or direct message other members.\n\n📙 **Channel Purpose**\nStick to the purpose of each channel. Be mindful of where you're posting.\n\n📙 **Staff Mentions**\nDo not mention Staff unless it's a true emergency.",
            inline=True,
        )

        embed.add_field(
            name="RULES",
            value="📗 **Basic Knowledge Required**\nA decent understanding of Lua, JavaScript, HTML, and CSS is expected. Take time to learn the basics before asking for help in ⁠support.\n\n📗 **Relevant Channels Only:**\nAsk questions in the correct channels. Avoid asking for help in non-support channels.",
            inline=True,
        )
        await interaction.response.send_message(embed=embed, view=RulesView())

    @app_commands.command(
        name="create_embed", description="Create a custom embed (Admin only)"
    )
    @app_commands.checks.has_any_role(*settings.EMBED_CREATOR_ROLES)
    async def create_embed(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Click the button to create an embed.",
            view=EmbedCreationView(),
            ephemeral=True,
        )

    @create_embed.error
    async def create_embed_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingAnyRole):
            await interaction.response.send_message(
                "You don't have permission to create embeds.", ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(EmbedCommands(bot))
