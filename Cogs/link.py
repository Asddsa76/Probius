import discord
from discord.ext import commands
from discord_slash import SlashCommandOptionType, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

base = "link"
servers = [437557557486288897]

class Link(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Module loaded: link")
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "build",
        guild_ids = servers,
        description = "Get a link to a Build.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "source",
                description = "Select a site or author.",
                required = False,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "Icy Veins",
                        value = "Icy Veins"
                    ),
                    create_choice(
                        name = "MindHawk",
                        value = "MindHawk"
                    )
                ]
            )
        ]
    )
    async def build(
        self,
        context: SlashContext,
        hero: str,
        source: str = None
    ):
        message = "Command used: /" + base + " build"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "guide",
        guild_ids = servers,
        description = "Get a link to a guide.",
        options = [
            create_option(
                name = "title",
                description = "Search for a string in their titles.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def guide(
        self,
        context: SlashContext,
        title: str
    ):
        message = "Command used: /" + base + " guide"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "reddit",
        guild_ids = servers,
        description = "Get a link to a Reddit post.",
        options = [
            create_option(
                name = "title",
                description = "Search for a string in their titles.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def reddit(
        self,
        context: SlashContext,
        title: str
    ):
        message = "Command used: /" + base + " reddit"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "tier-list",
        guild_ids = servers,
        description = "Get a link to a Tier List.",
        options = [
            create_option(
                name = "title",
                description = "Select a Tier List.",
                required = False,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "ARAM Tier List",
                        value = "ARAM Tier List"
                    ),
                    create_choice(
                        name = "General Tier List",
                        value = "General Tier List"
                    ),
                    create_choice(
                        name = "Master Tier List",
                        value = "Master Tier List"
                    )
                ]
            )
        ]
    )
    async def tierlist(
        self,
        context: SlashContext,
        title: str = None
    ):
        message = "Command used: /" + base + " tierlist"
        await context.send(content = message)
        print(message)
        
def setup(client):
    client.add_cog(Link(client))