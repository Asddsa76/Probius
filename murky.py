import discord
import os
from discord.ext import commands

from discord_slash import SlashCommand  # pip install -U discord-py-slash-command

from config import prefix, token

print("Now loading...")

message = f"__**Draft**__ \nban coin help map pick start undo"
message += f"\n__**Hero**__ \nability emoji info key level overview quote talent tooltip"
message += f"\n__**Link**__ \nbuild guide reddit tier-list"
message += f"\n__**Patch**__ \nindex text"
message += f"\n__**Pokedex**__ \nadd remove who"
message += f"\n__**Tool**__ \nbonk help pet poll summon vote"
message += f"\n__**User**__ \navatar color sort unsorted"
message += f"\n__**View**__ \ncore-ability role rotation"

class CustomHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        await self.get_destination().send(message)

    async def send_cog_help(self, cog):
        await self.get_destination().send(message)

    async def send_group_help(self, group):
        await self.get_destination().send(message)

    async def send_command_help(self, command):
        await self.get_destination().send(message)

client = commands.Bot(command_prefix = prefix, case_insensitive = True, help_command = CustomHelpCommand())

# How to setup Slash Commands
# 1. Discord Developer Portal > OAuth2 > Scopes: bot; applications.commands > Copy
# 2. Open the link with your browser to invite the bot to your Discord Server
slash = SlashCommand(client, sync_commands = True)

@client.command(brief = "Loads extension", description = "Loads a specific extension")
@commands.is_owner()
async def load(context, extension):
    client.load_extension(f'Cogs.{extension}')
    message = "Module loaded: " + extension
    print(message)

@client.command(brief = "Reloads extension", description = "Unloads and loads a specific extension")
@commands.is_owner()
async def reload(context, extension):
    client.unload_extension(f'Cogs.{extension}')
    client.load_extension(f'Cogs.{extension}')
    message = "Module reloaded: " + extension
    print(message)

@client.command(brief = "Unloads extension", description = "Unloads a specific extension")
@commands.is_owner()
async def unload(context, extension):
    client.unload_extension(f'Cogs.{extension}')
    message = "Module unloaded: " + extension
    print(message)

for file in os.listdir("./Cogs"):
    if file.endswith('.py'):
        client.load_extension(f'Cogs.{file[:-3]}')

@client.event
async def on_ready():
    message = "Core loaded."
    print(message)

@client.event
async def on_member_join(member):
    message = f"{member} has joined."
    await context.send(content = message)
    print(message)

@client.event
async def on_member_remove(member):
    message = f"{member} has left."
    await context.send(content = message)
    print(message)

@client.command()
@commands.has_role("Test")
async def hello(context):
    message = "Mmmrrrlllggg!"
    await context.send(content = message)
    print(message)

client.run(token)