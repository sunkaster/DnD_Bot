''' 
Discord Formatting Options:
Bold: **text**
Italic: *text*
Underline: __text__
Strikethrough: ~~text~~s
Spoiler: ||text||
The triple backticks (```) create the gray textbox effect you're looking for!
'''

import dice_roller
import character_creator
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import quotes

# Load environmental variables into system and check if the variable is loaded
load_result = load_dotenv()
api_key = os.environ.get('DISCORD_API_KEY')
if not api_key:
    print("ERROR: DISCORD_API_KEY environment variable not found!")
    print("Make sure the .env file exists with DISCORD_API_KEY=your_token_here")
    exit(1)

# Discord intents
intents=discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Initialize quote cache
quote_cache = quotes.QuoteCache()

# Runs once during startup
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to discord')
    # Sync slash commands
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.custom, name="Pondering", state="How does Ash always have a fish ready to eat? Where do they come from? ERROR:404 ¤=¤"))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Runs when and event occurs in the guild(Server) 
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # This line is REQUIRED when using commands.Bot to process slash commands. Here if we need to use event handlers like on_message, on_ready, on_member_join, etc.
    await bot.process_commands(message)
    
    """# Check if a massage starts with a bot command then run command !!!LEGACY BOT COMMANDS!!!
    for command in COMMANDS_LIST:
        if message.content.startswith(f'{command}'):
            # If command is a message then reply with the reply
            if COMMANDS_LIST[command]['type'] == "message":
                await message.channel.send(f'{COMMANDS_LIST[command]["reply"]}')
            # If a command contains the DiceRoll type then run the dice roller module
            if COMMANDS_LIST[command]['type'] == "DiceRoll":
                messageContent = message.content
                dice_roller_instance = dice_Roller.Dice_Roller()
                results = dice_roller_instance.roll_dice(messageContent, command)
                x = "\n".join(results)
                await message.channel.send(f'{x}')
            break"""

# "Slash commands"
#--------------------------------------
# Dice roller command
@bot.tree.command(name="roll", description="Roll dice (e.g., '1d8,(1d20)x2,2d6+5' )")
async def roll_slash(interaction: discord.Interaction, dice: str):
    """Slash command for rolling dice"""
    try:
        dice_roller_instance = dice_roller.Dice_Roller()
        results = dice_roller_instance.roll_dice(dice)
        x = "\n".join(results)
        await interaction.response.send_message(f">>> {x}")
    except Exception as e:
        await interaction.response.send_message(f"Error rolling dice: {e}")

# stat generation (4d6_drop_lowest)
@bot.tree.command(name="4d6_drop_lowest", description="Rolls 4d6 and drops the lowest stat. Returns Rolled values and total scores in size order")
async def ccFourDSix_slash(interaction: discord.Interaction):
    """Slash command for character creation based on 4d6 drop lowest method."""
    try:
        fourDSixDropLowest = character_creator.Character_Creator()
        stringResult, total_sum_rows = fourDSixDropLowest.roll_stats_FourDSix()
        await interaction.response.send_message(f">>> ## Character Stats Rolled \n-# Using 4d6_drop_lowest system \n \n{stringResult}\n Sum of all stats: {total_sum_rows}")
    except Exception as e:
        await interaction.response.send_message(f"Error rolling dice: {e}")

# Stat generation (StaticBase+DiceModifer)
@bot.tree.command(name="base_modifier_dice", description="Takes a base value(ex. 13) and dice(ex. d6). Returns (base+roll1-roll2=result)x6")
async def ccFourDSix_slash(interaction: discord.Interaction, base: int = 13, dice: str = "d6"):
    """Slash command for character creation Takes a base value and dice. Returns base+roll1-roll2=result"""
    try:
        base_modifier_dice = character_creator.Character_Creator()
        result, stat_total = base_modifier_dice.base_modifier_dice(base, dice)
        result_string = "\n".join(result)
        await interaction.response.send_message(f">>> ## Character Stats Rolled \n-# Using base_modifier_dice system\n\n{result_string}\n\nSum of all stats: {stat_total}")
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")

# Add this slash command to your bot
@bot.tree.command(name="inspire_me", description="Get the daily or a random inspiring quote from BOB himself")
async def quote_slash(interaction: discord.Interaction, type: str = "random"):
    """Slash command for getting quotes"""
    try:
        if type.lower() == "daily":
            quote = quote_cache.get_daily_quote()
        else:
            quote = quote_cache.get_random_quote()
        
        if quote:
            quote_text = quote['text']
            quote_author = quote['author']
            
            # Format the quote nicely
            formatted_quote = f"*\"{quote_text}\"*\n\n— by **BOB** ||(Actually: **{quote_author}**)||"
            await interaction.response.send_message(formatted_quote)
        else:
            await interaction.response.send_message(">>> Sorry, I was busy pondering another question currently, ask me again later.\n(couldn't fetch a quote right now.)")
            
    except Exception as e:
        await interaction.response.send_message(f"Error fetching quote: {e}")

# Hello
@bot.tree.command(name="hello", description="say hello")
async def hello_slash(interaction: discord.Interaction):
    """Simple hello slash command"""
    await interaction.response.send_message("Hello!")
#----------------------------------------

bot.run(api_key)

"""program_should_close = False
while not program_should_close: {
    

}"""