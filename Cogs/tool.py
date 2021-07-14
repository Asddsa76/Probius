import discord
import os
from discord.ext import commands

from discord_slash import SlashCommandOptionType, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

from config import servers

base = "tool"

class Tool(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Module loaded: tool")

    @cog_ext.cog_subcommand(
        base = base,
        name = "bonk",
        guild_ids = servers,
        description = "Bonk our little bot."
    )
    async def bonk(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " bonk"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "pet",
        guild_ids = servers,
        description = "Pet our little bot."
    )
    async def pet(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " pet"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "poll",
        guild_ids = servers,
        description = "Attach a poll to a new message.",
        options = [
            create_option(
                name = "options",
                description = "Select how many options you want.",
                required = True,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "2",
                        value = "2"
                    ),
                    create_choice(
                        name = "3",
                        value = "3"
                    ),
                    create_choice(
                        name = "4",
                        value = "4"
                    ),
                    create_choice(
                        name = "5",
                        value = "5"
                    ),
                    create_choice(
                        name = "6",
                        value = "6"
                    ),
                    create_choice(
                        name = "7",
                        value = "7"
                    ),
                    create_choice(
                        name = "8",
                        value = "8"
                    ),
                    create_choice(
                        name = "9",
                        value = "9"
                    )
                ]
            ),
            create_option(
                name = "message",
                description = "Write your message.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def poll(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " poll"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "summon",
        guild_ids = servers,
        description = "Pet our little bot."
    )
    async def summon(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " summon"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name = "vote",
        guild_ids = servers,
        description = "Attach a vote system to a new message.",
        options = [
            create_option(
                name = "message",
                description = "Write your message.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def vote(
        self,
        context: SlashContext
    ):
        message = "Command used: /" + base + " vote"
        await context.send(content = message)
        print(message)

def setup(client):
    client.add_cog(Tool(client))