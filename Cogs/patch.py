import discord
import os
from discord.ext import commands

from discord_slash import SlashCommandOptionType, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

from config import servers

base = "patch"

class Patch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Module loaded: patch")

    @cog_ext.cog_subcommand(
        base = base,
        name = "text",
        guild_ids = servers,
        description = "Search text within Patch Notes.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "text",
                description = "Search based on text.",
                required = False,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def text(
        self,
        context: SlashContext,
        hero: str,
        index: int = None,
        text: str = None
    ):
        message = "Command used: /" + base + " text"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "index",
        guild_ids = servers,
        description = "Look for Patch Notes.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "index",
                description = "Choose the x most recent result.",
                required = False,
                option_type = SlashCommandOptionType.INTEGER
            )
        ]
    )
    async def index(
        self,
        context: SlashContext,
        hero: str,
        index: int = None,
        text: str = None
    ):
        message = "Command used: /" + base + " index"
        await context.send(content = message)
        print(message)

def setup(client):
    client.add_cog(Patch(client))