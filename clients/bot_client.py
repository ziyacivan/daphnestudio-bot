import discord
from ui.views import LinksView, RulesView


class BotClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == "!links":
            await message.channel.send(view=LinksView())

        if message.content == "!rules":
            embed = discord.Embed(
                title="Daphne Studio - Server Rules",
                description="Click the **I have read and accept the rules.** button below to get access to the server.",
                color=discord.Color.dark_grey(),
            )

            embed.add_field(
                name="Discord Rules",
                value="Follow Discord’s Terms of Service and Community Guidelines.\n[Terms of Service](https://discord.com/terms) | [Community Guidelines](https://discordapp.com/guidelines)",
                inline=False,
            )

            embed.add_field(
                name="STICK",
                value="📕 **English-Only Chat**\nThis is an international community; please keep all conversations and questions in English. Using a translator is fine.\n\n📕 **Avoid Spam & Toxicity**\nSpamming, aggressive behavior, or toxic discussions will not be tolerated.\n\n📕 **Impersonation**\nImpersonating other users, bots, or public figures is strictly prohibited.",
                inline=True,
            )

            embed.add_field(
                name="TO THE",
                value="📙 **Respect & Maturity**\nMaintain a respectful and mature tone in all conversations. No excessive profanity, hate speech, harassment, or personal attacks. Do not randomly tag or direct message other members.\n\n📙 **Channel Purpose**\nStick to the purpose of each channel. Be mindful of where you’re posting.\n\n📙 **Staff Mentions**\nDo not mention Staff unless it’s a true emergency.",
                inline=True,
            )

            embed.add_field(
                name="RULES",
                value="📗 **Basic Knowledge Required**\nA decent understanding of Lua, JavaScript, HTML, and CSS is expected. Take time to learn the basics before asking for help in ⁠support.\n\n📗 **Relevant Channels Only:**\nAsk questions in the correct channels. Avoid asking for help in non-support channels.",
                inline=True,
            )
            await message.channel.send(embed=embed, view=RulesView())
