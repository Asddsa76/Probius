import discord, os
from discord.ext import commands
from discord_slash import SlashCommand # pip install -U discord-py-slash-command
from pathlib import Path
from ruamel.yaml import YAML # pip install ruamel.yaml

print("Now loading...")

root = os.path.abspath(os.curdir)
path = Path(root.replace(os.sep, "/") + "/config.yml")
yaml = YAML(typ = "safe")
data = yaml.load(path)

prefix = data["Prefix"]
token = os.getenv(data["Token"])

# How to setup Slash Commands
# 1. Discord Developer Portal > OAuth2 > Scopes: bot; applications.commands > Copy
# 2. Open the link with your browser to invite the bot to your Discord Server
client = commands.Bot(command_prefix = prefix, description = "Mmmrrrlllggg!", case_insensitive = True)
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
    
for file in os.listdir("./Cogs"):
    if file.endswith('.py'):
        client.load_extension(f'Cogs.{file[:-3]}')
        
@client.event
async def on_ready():
    print("Core loaded.")
    
client.run(token)