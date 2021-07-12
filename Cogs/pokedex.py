import discord, os
from discord.ext import commands
from discord_slash import SlashCommandOptionType, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from pathlib import Path
from ruamel.yaml import YAML # pip install ruamel.yaml

root = os.path.abspath(os.curdir)
path = Path(root.replace(os.sep, '/') + "/config.yml")
yaml = YAML(typ="safe")
data = yaml.load(path)

servers = data["Servers"]
base = "pokedex"

class Pokedex(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Module loaded: pokedex")

    @cog_ext.cog_subcommand(
        base = base,
        name = "add",
        guild_ids = servers,
        description = "Add a player to Pokedex.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "player",
                description = "Write the name of a player.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def add(
        self,
        context: SlashContext,
        hero: str,
        player: str
    ):
        message = "Command used: /" + base + " add"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "remove",
        guild_ids = servers,
        description = "Remove a player from Pokedex.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "player",
                description = "Write the name of a player.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )    
    async def remove(
        self,
        context: SlashContext,
        hero: str,
        player: str
    ):
        message = "Command used: /" + base + " remove"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "who",
        guild_ids = servers,
        description = "List all experts about a Hero.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )    
    async def pokedex(
        self,
        context: SlashContext,
        hero: str
    ):
        message = "Command used: /" + base + " who"
        await context.send(content = message)
        print(message)
        
def setup(client):
    client.add_cog(Pokedex(client))