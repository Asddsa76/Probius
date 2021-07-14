import discord
import os
from discord.ext import commands

from discord_slash import SlashCommandOptionType, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

from config import servers

base = "user"

class User(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Module loaded: user")
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "avatar",
        guild_ids = servers,
        description = "Enhance!"
    )
    async def avatar(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " avatar"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "color",
        guild_ids = servers,
        description = "Show all the colors available for nicknames."
    )
    async def color(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " color"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "sort",
        guild_ids = servers,
        description = "Sort yourself to gain full access to this Discord server.",
        options = [
            create_option(
                name = "server",
                description = "Select your main in-game Server (Region).",
                required = True,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "Europe (Europe)",
                        value = "EU"
                    ),
                    create_choice(
                        name = "North America (Americas)",
                        value = "NA"
                    ),
                    create_choice(
                        name = "Singapore (Americas)",
                        value = "SG"
                    ),
                    create_choice(
                        name = "Brazil (Americas)",
                        value = "LA"
                    ),
                    create_choice(
                        name = "Australia (Americas)",
                        value = "OC"
                    ),
                    create_choice(
                        name = "Taiwan (Asia)",
                        value = "TW"
                    ),
                    create_choice(
                        name = "Korea (Asia)",
                        value = "KR"
                    ),
                    create_choice(
                        name = "China (China)",
                        value = "CH"
                    )
                ]
            ),
            create_option(
                name = "rank",
                description = "Select your highest Rank ever.",
                required = True,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "Grand Master",
                        value = "Grand Master"
                    ),
                    create_choice(
                        name = "Master",
                        value = "Master"
                    ),
                    create_choice(
                        name = "Diamond",
                        value = "Diamond"
                    ),
                    create_choice(
                        name = "Platinum",
                        value = "Platinum"
                    ),
                    create_choice(
                        name = "Gold",
                        value = "Gold"
                    ),
                    create_choice(
                        name = "Silver",
                        value = "Silver"
                    ),
                    create_choice(
                        name = "Bronze",
                        value = "Bronze"
                    ),
                    create_choice(
                        name = "Wood",
                        value = "Wood"
                    ),
                    create_choice(
                        name = "None",
                        value = "Unranked"
                    )
                ]
            ),
            create_option(
                name = "color",
                description = "Choose a color for your nickname.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def sort(
        self,
        context: SlashContext,
        server: str,
        rank: str,
        color: str
    ):
        message = "Command used: /" + base + " sort"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "unsorted",
        guild_ids = servers,
        description = "Invite unsorted members to register."
    )
    async def unsorted(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " unsorted"
        await context.send(content = message)
        print(message)

def setup(client):
    client.add_cog(User(client))