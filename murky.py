import discord, os
from discord.ext import commands
from discord_slash import SlashCommand

#Documentation for Slash Commands
#https://discord-py-slash-command.readthedocs.io/en/latest/gettingstarted.html
#https://discord.com/developers/docs/interactions/slash-commands

print("Now loading...")
token = "ODYyNjA1ODk1ODU4MTI2ODQ5.YOayWA.88tvq7lslqKcNxnB_lkXt9INKww"

client = commands.Bot(command_prefix = ("/"))
slash = SlashCommand(client, sync_commands = True)

@client.command(brief = "Loads extension", description = "Loads a specific extension")
async def load(context, extension):
    client.load_extension(f'Cogs.{extension}')
    print("Module loaded: " + extension)
    
@client.command(brief = "Reloads extension", description = "Unloads and loads a specific extension")
async def reload(context, extension):
    client.unload_extension(f'Cogs.{extension}')
    client.load_extension(f'Cogs.{extension}')
    print("Module reloaded: " + extension)
    
@client.command(brief = "Unloads extension", description = "Unloads a specific extension")
async def unload(context, extension):
    client.unload_extension(f'Cogs.{extension}')
    print("Module unloaded: " + extension)
    
for file in os.listdir("C:/Users/Michele/Desktop/Murky/Cogs"):
    if file.endswith('.py'):
        client.load_extension(f'Cogs.{file[:-3]}')
        
@client.event
async def on_ready():
    print("Core loaded.")
    
client.run(token)