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
import discord
from discord.ext import commands

# Gets api key from the enviromental virable DISCORD_API_KEY
api_key=os.environ['DISCORD_API_KEY']

# Discord intents
intents=discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# Runs once during startup
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to discord')
    # Sync slash commands
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
@bot.tree.command(name="roll", description="Roll dice (e.g., (2d10)x2,2d8 + 5d6, 1d8 )")
async def roll_slash(interaction: discord.Interaction, dice: str):
    """Slash command for rolling dice"""
    try:
        dice_roller_instance = dice_roller.Dice_Roller()
        results = dice_roller_instance.roll_dice(dice)
        x = "\n\n".join(results)
        await interaction.response.send_message(f">>> {x}")
    except Exception as e:
        await interaction.response.send_message(f"Error rolling dice: {e}")

# Character Stats command
@bot.tree.command(name="4d6_drop_lowest", description="Rolls 4d6 and drops the lowest stat. Returns Rolled values and total scores in size order")
async def ccFourDSix_slash(interaction: discord.Interaction):
    """Slash command for character creation based on 4d6 drop lowest method."""
    try:
        fourDSixDropLowest = character_creator.Character_Creator()
        stringResult, total_sum_rows = fourDSixDropLowest.roll_stats_FourDSix()
        await interaction.response.send_message(f">>> \n{stringResult}\n Sum of all stats: {total_sum_rows}")
    except Exception as e:
        await interaction.response.send_message(f"Error rolling dice: {e}")

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