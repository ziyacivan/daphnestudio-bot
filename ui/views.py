import discord


class LinksView(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.Button(label="Website", url="https://daphnestudio.net")
        )
        self.add_item(
            discord.ui.Button(label="Docs", url="https://docs.daphnestudio.net")
        )
        self.add_item(
            discord.ui.Button(
                label="YouTube", url="https://www.youtube.com/@daphne-studio"
            )
        )
        self.add_item(
            discord.ui.Button(label="Discord", url="https://discord.gg/daphne")
        )
        self.add_item(
            discord.ui.Button(
                label="GitHub", url="https://github.com/orgs/daphne-studio/"
            )
        )


class RulesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="I have read and accept the rules.",
        style=discord.ButtonStyle.primary,
        custom_id="accept_rules",
    )
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        ROLE_ID = 1456815542148137030
        role = interaction.guild.get_role(ROLE_ID)

        if role:
            try:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(
                    "Thank you for accepting the rules! You have been granted access to the server.",
                    ephemeral=True,
                )
            except discord.Forbidden:
                await interaction.response.send_message(
                    "Error: I do not have permission to assign roles.",
                    ephemeral=True,
                )
        else:
            await interaction.response.send_message(
                "Error: I cannot find the role.", ephemeral=True
            )
