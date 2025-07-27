import random
import userInput
from Bot_Commands import COMMANDS_LIST
import dice_Roller
import os
import discord

# Gets api key from the enviromental virable DISCORD_API_KEY
api_key=os.environ['DISCORD_API_KEY']

# Discord intents
intents=discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Runs once during startup
@client.event
async def on_ready():
    print(f'{client.user} has connected to discord')

# Runs when and event occurs in the guild(Server) 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # Check if a massage starts with a bot command then run command
    for command in COMMANDS_LIST:
        if message.content.startswith(f'{command}'):
            # If command is a message then reply with the reply
            if COMMANDS_LIST[command]['type'] == "message":
                await message.channel.send(f'{COMMANDS_LIST[command]["reply"]}')
            
            if COMMANDS_LIST[command]['type'] == "DiceRoll":
                messageContent = message.content
                dice_roller_instance = dice_Roller.Dice_Roller()
                results = dice_roller_instance.roll_dice(messageContent, command)
                x = "\n".join(results)
                await message.channel.send(f'{x}')
                
            break
        

client.run(api_key)

"""program_should_close = False
while not program_should_close: {
    

}"""