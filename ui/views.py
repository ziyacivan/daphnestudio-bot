import discord
from config import settings


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


class EmbedCreationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Embed", style=discord.ButtonStyle.primary)
    async def create_embed(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        modal = EmbedCreationModal()
        await interaction.response.send_modal(modal)


class EmbedCreationModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Create Embed")

        self.title_input = discord.ui.TextInput(
            label="Title", placeholder="Embed title", required=True
        )
        self.description_input = discord.ui.TextInput(
            label="Description",
            placeholder="Embed description",
            style=discord.TextStyle.paragraph,
            required=False,
        )
        self.image_input = discord.ui.TextInput(
            label="Image URL",
            placeholder="https://example.com/image.png",
            required=False,
        )
        self.color_input = discord.ui.TextInput(
            label="Color (hex)", placeholder="#5865F2", required=False, max_length=7
        )

        self.add_item(self.title_input)
        self.add_item(self.description_input)
        self.add_item(self.image_input)
        self.add_item(self.color_input)

    async def on_submit(self, interaction: discord.Interaction):
        color = discord.Color.blue()
        if self.color_input.value:
            try:
                color = discord.Color(int(self.color_input.value.replace("#", ""), 16))
            except:
                pass

        embed = discord.Embed(
            title=self.title_input.value,
            description=self.description_input.value or None,
            color=color,
        )

        if self.image_input.value:
            embed.set_image(url=self.image_input.value)

        view = EmbedBuilderView(embed)
        await interaction.response.send_message(
            "**Preview:** (Use buttons below to edit)",
            embed=embed,
            view=view,
            ephemeral=True,
        )


class AddFieldModal(discord.ui.Modal):
    def __init__(self, embed_data):
        super().__init__(title="Add Field")
        self.embed_data = embed_data

        self.field_name = discord.ui.TextInput(
            label="Field Name", placeholder="Enter field name", required=True
        )
        self.field_value = discord.ui.TextInput(
            label="Field Value",
            placeholder="Enter field value",
            style=discord.TextStyle.paragraph,
            required=True,
        )
        self.inline_input = discord.ui.TextInput(
            label="Inline? (yes/no)", placeholder="no", required=False, max_length=3
        )

        self.add_item(self.field_name)
        self.add_item(self.field_value)
        self.add_item(self.inline_input)

    async def on_submit(self, interaction: discord.Interaction):
        inline = self.inline_input.value.lower() in ["yes", "y", "true"]
        self.embed_data["fields"].append(
            {
                "name": self.field_name.value,
                "value": self.field_value.value,
                "inline": inline,
            }
        )

        embed = discord.Embed(
            title=self.embed_data["title"],
            description=self.embed_data["description"],
            color=self.embed_data["color"],
        )

        if self.embed_data.get("image"):
            embed.set_image(url=self.embed_data["image"])

        for field in self.embed_data["fields"]:
            embed.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )

        view = EmbedBuilderView(self.embed_data)
        await interaction.response.edit_message(
            content="**Preview:** (Use buttons below to edit)", embed=embed, view=view
        )


class EmbedBuilderView(discord.ui.View):
    def __init__(self, embed_data):
        super().__init__(timeout=None)
        if isinstance(embed_data, discord.Embed):
            self.embed_data = {
                "title": embed_data.title,
                "description": embed_data.description,
                "color": embed_data.color,
                "image": embed_data.image.url if embed_data.image else None,
                "fields": [],
            }
        else:
            self.embed_data = embed_data

    @discord.ui.button(label="Add Field", style=discord.ButtonStyle.primary)
    async def add_field(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if not any(
            role.id in settings.EMBED_CREATOR_ROLES for role in interaction.user.roles
        ):
            await interaction.response.send_message(
                "You don't have permission to use this.", ephemeral=True
            )
            return
        modal = AddFieldModal(self.embed_data)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Publish", style=discord.ButtonStyle.success)
    async def publish_embed(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if not any(
            role.id in settings.EMBED_CREATOR_ROLES for role in interaction.user.roles
        ):
            await interaction.response.send_message(
                "You don't have permission to use this.", ephemeral=True
            )
            return

        embed = discord.Embed(
            title=self.embed_data["title"],
            description=self.embed_data["description"],
            color=self.embed_data["color"],
        )

        if self.embed_data.get("image"):
            embed.set_image(url=self.embed_data["image"])

        for field in self.embed_data["fields"]:
            embed.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )

        view = DynamicEmbedView(self.embed_data)
        await interaction.channel.send(embed=embed, view=view)
        await interaction.response.edit_message(
            content="✅ Embed published!", embed=None, view=None
        )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel_embed(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.edit_message(
            content="❌ Cancelled", embed=None, view=None
        )


class EditEmbedModal(discord.ui.Modal):
    def __init__(self, current_embed_data):
        super().__init__(title="Edit Embed")
        self.embed_data = current_embed_data

        self.title_input = discord.ui.TextInput(
            label="Title",
            placeholder="Embed title",
            default=current_embed_data.get("title", ""),
            required=True,
        )
        self.description_input = discord.ui.TextInput(
            label="Description",
            placeholder="Embed description",
            style=discord.TextStyle.paragraph,
            default=current_embed_data.get("description", ""),
            required=False,
        )
        self.image_input = discord.ui.TextInput(
            label="Image URL",
            placeholder="https://example.com/image.png",
            default=current_embed_data.get("image", ""),
            required=False,
        )
        self.color_input = discord.ui.TextInput(
            label="Color (hex)",
            placeholder="#5865F2",
            default=(
                f"#{current_embed_data.get('color', discord.Color.blue()).value:06x}"
                if current_embed_data.get("color")
                else ""
            ),
            required=False,
            max_length=7,
        )

        self.add_item(self.title_input)
        self.add_item(self.description_input)
        self.add_item(self.image_input)
        self.add_item(self.color_input)

    async def on_submit(self, interaction: discord.Interaction):
        color = discord.Color.blue()
        if self.color_input.value:
            try:
                color = discord.Color(int(self.color_input.value.replace("#", ""), 16))
            except:
                pass

        self.embed_data["title"] = self.title_input.value
        self.embed_data["description"] = self.description_input.value or None
        self.embed_data["color"] = color
        self.embed_data["image"] = self.image_input.value or None

        embed = discord.Embed(
            title=self.embed_data["title"],
            description=self.embed_data["description"],
            color=self.embed_data["color"],
        )

        if self.embed_data.get("image"):
            embed.set_image(url=self.embed_data["image"])

        for field in self.embed_data.get("fields", []):
            embed.add_field(
                name=field["name"], value=field["value"], inline=field["inline"]
            )

        view = DynamicEmbedView(self.embed_data)
        await interaction.message.edit(embed=embed, view=view)
        await interaction.response.send_message("✅ Embed updated!", ephemeral=True)


class DynamicEmbedView(discord.ui.View):
    def __init__(self, embed_data=None):
        super().__init__(timeout=None)
        self.embed_data = embed_data or {"fields": []}
