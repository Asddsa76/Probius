import discord
import os
from discord.ext import commands

from discord_slash import SlashCommandOptionType, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

from config import servers

base = "hero"

class Hero(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Module loaded: hero")

    @cog_ext.cog_subcommand(
        base = base,
        name = "ability",
        guild_ids = servers,
        description = "Search for Abilities based on name.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "ability",
                description = "Choose an Ability by writing their name or part of it..",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def ability(
        self,
        context: SlashContext,
        hero: str,
        ability: str,
    ):
        message = "Command used: /" + base + " ability"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "emoji",
        guild_ids = servers,
        description = "Use in-game Emojis here on Discord.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "emotion",
                description = "Select an emotion.",
                required = False,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "Angry",
                        value = "angry"
                    ),
                    create_choice(
                        name = "Cool",
                        value = "cool"
                    ),
                    create_choice(
                        name = "Happy",
                        value = "happy"
                    ),
                    create_choice(
                        name = "Laugh",
                        value = "lol"
                    ),
                    create_choice(
                        name = "Love",
                        value = "love"
                    ),
                    create_choice(
                        name = "Meh",
                        value = "meh"
                    ),
                    create_choice(
                        name = "Oops",
                        value = "oops"
                    ),
                    create_choice(
                        name = "Sad",
                        value = "sad"
                    ),
                    create_choice(
                        name = "Silly",
                        value = "silly"
                    ),
                    create_choice(
                        name = "Wow",
                        value = "wow"
                    )
                ]
            )
        ]
    )
    async def emoji(
        self,
        context: SlashContext,
        hero: str,
        emotion: str = None,
    ):
        message = "Command used: /" + base + " emoji"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "info",
        guild_ids = servers,
        description = "Show the in-game values of a given Hero.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def info(
        self,
        context: SlashContext,
        hero: str
    ):
        message = "Command used: /" + base + " info"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "key",
        guild_ids = servers,
        description = "Search for Abilities based on key.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "key",
                description = "Select a key.",
                required = True,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "Q",
                        value = "Q"
                    ),
                    create_choice(
                        name = "W",
                        value = "W"
                    ),
                    create_choice(
                        name = "E",
                        value = "E"
                    ),
                    create_choice(
                        name = "R",
                        value = "R"
                    ),
                    create_choice(
                        name = "D",
                        value = "D"
                    ),
                    create_choice(
                        name = "1",
                        value = "1"
                    )
                ]
            )
        ]
    )
    async def key(
        self,
        context: SlashContext,
        hero: str,
        key: str
    ):
        message = "Command used: /" + base + " key"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "level",
        guild_ids = servers,
        description = "Search for Talents based on Level.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "level",
                description = "Select a Level.",
                required = True,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "1",
                        value = "1"
                    ),
                    create_choice(
                        name = "4",
                        value = "4"
                    ),
                    create_choice(
                        name = "7",
                        value = "7"
                    ),
                    create_choice(
                        name = "10",
                        value = "10"
                    ),
                    create_choice(
                        name = "13",
                        value = "13"
                    ),
                    create_choice(
                        name = "16",
                        value = "16"
                    ),
                    create_choice(
                        name = "20",
                        value = "20"
                    )
                ]
            )
        ]
    )
    async def level(
        self,
        context: SlashContext,
        hero: str,
        level: str
    ):
        message = "Command used: /" + base + " level"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "overview",
        guild_ids = servers,
        description = "Show the overview of a given Hero.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def overview(
        self,
        context: SlashContext,
        hero: str
    ):
        message = "Command used: /" + base + " overview"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "quote",
        guild_ids = servers,
        description = "Get a quote about a Hero.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def quote(
        self,
        context: SlashContext,
        hero: str
    ):
        message = "Command used: /" + base + " quote"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "talent",
        guild_ids = servers,
        description = "Search for Talents based on name.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "talent",
                description = "Choose a Talent by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def talent(
        self,
        context: SlashContext,
        hero: str,
        talent: str
    ):
        message = "Command used: /" + base + " talent"
        await context.send(content = message)
        print(message)

    @cog_ext.cog_subcommand(
        base = base,
        name = "tooltip",
        guild_ids = servers,
        description = "Search for Abilities and Talents based on tooltip.",
        options = [
            create_option(
                name = "hero",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            ),
            create_option(
                name = "tooltip",
                description = "Search based on text in tooltips.",
                required = True,
                option_type = SlashCommandOptionType.STRING
            )
        ]
    )
    async def tooltip(
        self,
        context: SlashContext,
        hero: str,
        tooltip: str
    ):
        message = "Command used: /" + base + " tooltip"
        await context.send(content = message)
        print(message)

def setup(client):
    client.add_cog(Hero(client))