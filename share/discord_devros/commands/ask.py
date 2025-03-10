import discord
from discord.ext import commands
from discord-devros.utils import query_openwebui

class AskCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ask')
    async def ask(self, ctx, *, question: str):
        username = ctx.author.name  # Get the username of the person asking
        
        # Prepare the prompt to include the username
        prompt = f"User {username} asks: {question}"
        
        try:
            # Send the request to Open WebUI and get the response (await it since it's an async function)
            response = await query_openwebui(prompt)  # Ensure this is awaited
            
            # Send the response back, tagging the user and including the response
            await ctx.send(f"{ctx.author.mention}, {response}")
        
        except Exception as e:
            # Handle any errors that occur with the Open WebUI query
            await ctx.send(f"Sorry {ctx.author.mention}, I encountered an error: {str(e)}")

# Updated setup function to be asynchronous
async def setup(bot):
    await bot.add_cog(AskCommand(bot))
