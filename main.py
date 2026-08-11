import json
import settings
import discord
from discord.ext import commands
from discord.errors import Forbidden
from discord import app_commands

GUILD_ID = int(settings.GUILD_ID)

def run():
    intents = discord.Intents.all()
    intents.message_content = True
    intents.members = True
    activity = discord.Activity(type=discord.ActivityType.playing, name='Work in Progress!')
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
        try:
            synced1guild = bot.get_guild(GUILD_ID)
            synced1 = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
            list1 = []
            for comm in synced1:
                list1.append(comm.name)
            print(f"Synced {str(list1)[1:-1]} ({len(synced1)}) slash commands in {synced1guild.name}")
        except Exception as e:
            print(f"Failed to sync slash commands: {e}")
            raise e
        print(f"Logged in as {bot.user}")

    @bot.command()
    async def ping(ctx):
        await ctx.reply("Pong!")

    bot.run(settings.DISCORD_API_SECRET)

if __name__ == "__main__":
    run()
