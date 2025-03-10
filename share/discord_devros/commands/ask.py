import discord
from discord.ext import commands
from discord_devros.utils import query_openwebui

class AskCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx, *, question: str):
        """Send a question to the OpenWebUI model and get an answer."""
        await ctx.send("Querying OpenWebUI...")

        # Query OpenWebUI for the answer
        result = query_openwebui(question)
        
        # Check if there's an error in the result
        if "error" in result:
            await ctx.send(f"Error: {result['error']}")
        else:
            # Assuming the response has a 'response' field with the model's answer
            await ctx.send(f"Answer: {result.get('response', 'No response from model.')}")
