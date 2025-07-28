# Discord D&D Bot

A Discord bot for Dungeons & Dragons with dice rolling and character creation features.

## Features

- **Dice Rolling**: Roll dice with complex expressions (e.g., `2d10`, `5d6+3`, `(2d10)x2`)
- **Character Creation**: Generate D&D character stats using 4d6 drop lowest method
- **Slash Commands**: Modern Discord slash command interface

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd DnD_Bot
```

### 2. Set Up Environment Variables
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and fill in your Discord bot credentials:
   - `DISCORD_API_KEY`: Your bot token from Discord Developer Portal
   - `DISCORD_APPLICATION_ID`: Your application ID
   - `DISCORD_PUBLIC_KEY`: Your bot's public key

### 3. Run with Docker (Recommended)
```bash
docker-compose up --build
```

### 4. Run without Docker
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the bot:
   ```bash
   python program.py
   ```

## Available Commands

- `/roll <dice>` - Roll dice (e.g., `/roll 2d10+5`)
- `/4d6_drop_lowest` - Generate D&D character stats
- `/hello` - Simple greeting command

## Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section and create a bot
4. Copy the bot token and add it to your `.env` file
5. Invite the bot to your server with appropriate permissions (Send Messages, Use Slash Commands)
