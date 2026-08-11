import discord
import discord.errors
from discord import app_commands
from discord.ext import commands

class ticket(commands.Cog, name="ticket"):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def pong(self, ctx):
        await ctx.reply("Ping!")
        await ctx.send(self.bot.user.mention)

async def setup(bot):
    await bot.add_cog(ticket(bot))
