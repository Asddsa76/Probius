import discord
import os
from discord.ext import commands

from discord_slash import SlashCommandOptionType, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

from config import servers

base = "mod"

class Mod(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Module loaded: mod")

    @cog_ext.cog_subcommand(
        base = base,
        name = "clear",
        guild_ids = servers,
        description = "Delete the latest x messages in the current channel.",
        options = [
            create_option(
                name = "amount",
                description = "Choose a Hero by writing their name or part of it.",
                required = True,
                option_type = SlashCommandOptionType.INTEGER
            )
        ]
    )
    @commands.has_permissions(manage_messages = True)
    async def clear(
        self,
        context,
        amount: int
    ):
        await context.channel.purge (limit = 1 + amount)
        if amount == 1:
            message = f"1 message deleted."
        else:
            message = f"{amount} messages deleted."
        await context.send(content = message)
        print(message)

def setup(client: commands.Bot):
    client.add_cog(Mod(client))