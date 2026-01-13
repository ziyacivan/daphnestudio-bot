# Daphne Studio Bot

A feature-rich Discord bot designed for the Daphne Studio community. This bot provides automated role management, custom embed creation, server rules management, and quick access to important community links.

## Features

- **Auto-Role Assignment**: Automatically assigns a role to new members when they join the server
- **Interactive Rules System**: Display server rules with an acceptance button that grants server access
- **Custom Embed Creator**: Advanced embed creation tool with fields, images, and customization options
- **Quick Links**: Easy access to Daphne Studio resources (Website, Docs, YouTube, Discord, GitHub)
- **Dynamic Embeds**: Create, edit, and manage embeds with interactive buttons
- **Permission Control**: Role-based access control for embed creation commands

## Prerequisites

- Python 3.14.2 or higher
- A Discord Bot Token
- Discord Server (Guild) ID

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/daphnestudio-bot.git
   cd daphnestudio-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```
   Or using uv:
   ```bash
   uv pip install -e .
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your Discord bot token and server ID
   ```bash
   cp .env.example .env
   ```

4. **Edit configuration**
   - Open `config/settings.py`
   - Update `AUTO_ROLE_ID` with your desired auto-role ID
   - Update `EMBED_CREATOR_ROLES` with role IDs that can create embeds

## Configuration

### Environment Variables

- `BOT_TOKEN`: Your Discord bot token (required)
- `GUILD_ID`: Your Discord server (guild) ID for instant command syncing

### Bot Settings

Located in `config/settings.py`:
- `AUTO_ROLE_ID`: Role automatically assigned to new members
- `EMBED_CREATOR_ROLES`: List of role IDs allowed to create and manage embeds

## Usage

Run the bot:
```bash
python main.py
```

### Available Commands

- `/links` - Display Daphne Studio important links (Website, Docs, YouTube, etc.)
- `/rules` - Display server rules with an acceptance button
- `/create_embed` - Open the embed creation interface (requires embed creator role)

## Project Structure

```
daphnestudio-bot/
├── clients/
│   ├── __init__.py
│   └── bot_client.py       # Main bot client with event handlers
├── commands/
│   ├── __init__.py
│   └── embed_commands.py   # Slash commands for embeds
├── config/
│   ├── __init__.py
│   └── settings.py         # Configuration and environment variables
├── ui/
│   ├── __init__.py
│   └── views.py            # Discord UI components (buttons, modals, views)
├── .env.example            # Example environment variables
├── main.py                 # Bot entry point
├── pyproject.toml          # Project dependencies
└── README.md               # This file
```

## Bot Permissions

The bot requires the following permissions:
- Manage Roles
- Send Messages
- Use Slash Commands
- Read Message History
- View Channels

## Development

The bot is built using:
- [discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable management

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See the [LICENSE](LICENSE) file for details.

## Support

For support, join the [Daphne Studio Discord](https://discord.gg/daphne) server.
