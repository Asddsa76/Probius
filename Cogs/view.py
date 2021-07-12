import discord
from discord.ext import commands
from discord_slash import SlashCommandOptionType, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option

base = "view"
servers = [437557557486288897]

class View(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Module loaded: view")
    
    @cog_ext.cog_subcommand(
        base = base,
        name = "core-ability",
        guild_ids = servers,
        description = "View the Core Ability for a Map.",
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
    async def core(
        self,
        context: SlashContext,
        map: str = None
    ):
        message = "Command used: /" + base + " core"
        await context.send(content = message)
        print(message)
    
    @cog_ext.cog_subcommand(
        base = base,
        name = "role",
        guild_ids = servers,
        description = "List all Heroes beloning to a Role.",
        options = [
            create_option(
                name="role",
                description = "Select a Role.",
                required = True,
                option_type = SlashCommandOptionType.STRING,
                choices = [
                    create_choice(
                        name = "Tank",
                        value = "Tank"
                    ),
                    create_choice(
                        name = "Bruiser",
                        value = "Bruiser"
                    ),
                    create_choice(
                        name = "Assassin",
                        value = "Assassin"
                    ),
                    create_choice(
                        name = "Marksman",
                        value = "Marksman"
                    ),
                    create_choice(
                        name = "Mage",
                        value = "Mage"
                    ),
                    create_choice(
                        name = "Support",
                        value = "Support"
                    ),
                    create_choice(
                        name = "Healer",
                        value = "Healer"
                    )
                ]
            )
        ]
    )
    async def role(
        self,
        context: SlashContext,
        role: str
    ):
        message = "Command used: /" + base + " role"
        await context.send(content = message)
        print(message)
        
    @cog_ext.cog_subcommand(
        base = base,
        name="rotation",
        guild_ids = servers,
        description="View a Rotation.",
        options=[
            create_option(
                name="type",
                description="Select a rotation.",
                required=True,
                option_type=SlashCommandOptionType.STRING,
                choices=[
                    create_choice(
                        name="Free Hero Rotation",
                        value="Free Hero Rotation"
                    ),
                    create_choice(
                        name="Ranked Map Rotation",
                        value="Ranked Map Rotation"
                    ),
                    create_choice(
                        name="Unranked Map Rotation",
                        value="Unranked Map Rotation"
                    ),
                    create_choice(
                        name="Sales Rotation",
                        value="Sales Rotation"
                    )
                ]
            )
        ]
    )
    async def rotation(
        self,
        context: SlashContext,
        type: str
    ):
        message = "Command used: /" + base + " rotation"
        await context.send(content = message)
        print(message)
        
def setup(client):
    client.add_cog(View(client))