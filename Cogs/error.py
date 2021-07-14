from discord.ext import commands

class Error(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Module loaded: error")
    
    @commands.Cog.listener()
    async def on_command_error(self, context: commands.Context, error: commands.CommandError):
        message = None
        if isinstance(error, commands.BadArgument):
            message = "Invalid argument."
        if isinstance(error, commands.CommandNotFound):
            message = "Command not found."
        if isinstance(error, commands.MissingPermissions):
            message = "No permissions."
        if isinstance(error, commands.MissingRole):
            message = "No permissions."
        if isinstance(error, commands.MissingRequiredArgument):
            message = "Missing required argument."
        if message == None:
            raise error
        else:
            await context.send(message)
            print (message)

def setup(client: commands.Bot):
    client.add_cog(Error(client))