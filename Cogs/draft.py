import discord, os
from discord.ext import commands
from discord_slash import SlashCommandOptionType, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from pathlib import Path
from ruamel.yaml import YAML # pip install ruamel.yaml

root = os.path.abspath(os.curdir)
path = Path(root.replace(os.sep, "/") + "/config.yml")
yaml = YAML(typ = "safe")
data = yaml.load(path)

servers = data["Servers"]
base = "draft"

class Draft(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Module loaded: draft")
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "ban",
        guild_ids = servers,
        description = "Ban a Hero.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def ban(
        self,
        context: SlashContext,
        hero: str
    ):
        message = "Command used: /" + base + " ban"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "coin",
        guild_ids = servers,
        description = "Toss a coin.",
        options = [
            create_option(
                name = "guess",
                description = "Guess the result.",
                required = False,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "Head",
                        value = "Head"
                    ),
                    create_choice(
                        name = "Tail",
                        value = "Tail"
                    )
                ]
            )
        ]
    )
    async def coin(
        self,
        context: SlashContext,
        guess: str = None
    ):
        message = "Command used: /" + base + " coin"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "help",
        guild_ids = servers,
        description = "Open the draft simulation guide."
    )
    async def guide(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " draft"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "map",
        guild_ids = servers,
        description = "Pick a Map.",
        options = [
            create_option(
                name = "map",
                description = "Choose a Map.",
                required = False,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "Alterac Pass",
                        value = "Alterac Pass"
                    ),
                    create_choice(
                        name = "Battlefield of Eternity",
                        value = "Battlefield of Eternity"
                    ),
                    create_choice(
                        name = "Blackheart's Bay",
                        value = "Blackheart's Bay"
                    ),
                    create_choice(
                        name = "Braxis Holdout",
                        value = "Braxis Holdout"
                    ),
                    create_choice(
                        name = "Cursed Hollow",
                        value = "Cursed Hollow"
                    ),
                    create_choice(
                        name = "Dragon Shire",
                        value = "Dragon Shire"
                    ),
                    create_choice(
                        name = "Garden of Terror",
                        value = "Garden of Terror"
                    ),
                    create_choice(
                        name = "Hanamura Temple",
                        value = "Hanamura Temple"
                    ),
                    create_choice(
                        name = "Infernal Shrines",
                        value = "Infernal Shrines"
                    ),
                    create_choice(
                        name = "Sky Temple",
                        value = "Sky Temple"
                    ),
                    create_choice(
                        name = "Tomb of the Spider Queen",
                        value = "Tomb of the Spider Queen"
                    ),
                    create_choice(
                        name = "Towers of Doom",
                        value = "Towers of Doom"
                    ),
                    create_choice(
                        name = "Volskaya Foundry",
                        value = "Volskaya Foundry"
                    ),
                    create_choice(
                        name = "Warhead Junction",
                        value = "Warhead Junction"
                    )
                ]
            )
        ]
    )
    async def map(
        self,
        context: SlashContext,
        map: str = None
    ):
        message = "Command used: /" + base + " map"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "pick",
        guild_ids = servers,
        description = "Pick a Hero.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def pick(
        self,
        context: SlashContext,
        hero: str = None
    ):
        message = "Command used: /" + base + " pick"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "start",
        guild_ids = servers,
        description = "Start a new draft."
    )
    async def start(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " start"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "undo",
        guild_ids = servers,
        description = "Undo previous move."
    )
    async def undo(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " undo"
        await context.send(content = message)
        print(message)
        
def setup(client):
    client.add_cog(Draft(client))
    
