import json
import settings
import discord
from discord.ext import commands
from discord.errors import Forbidden
from discord import app_commands

IEEM = 693193721612861511

def run():
    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True
    activity = discord.Activity(type=discord.ActivityType.playing, name='Testing')
    bot = commands.Bot(
        command_prefix='.',
        intents=intents,
        activity=activity,
        status=discord.Status.idle,
    )

    @bot.event
    async def on_ready():
        print(f"User: {bot.user} (ID: {bot.user.id})")
        for cmd_file in settings.CMDS_DIR.glob("*.py"):
            if cmd_file.name != "__init__.py":
                await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
                print(f"{cmd_file.name[:-3]} loaded!")
        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")
                print(f"{cog_file.name[:-3]} loaded!")

    @bot.command()
    async def ping(ctx):
        await ctx.reply("Pong!")

    bot.run(settings.DISCORD_API_SECRET)

if __name__ == "__main__":
    run()
