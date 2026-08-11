import os
import discord
import pathlib
from dotenv import load_dotenv

load_dotenv()
DISCORD_API_SECRET=os.getenv("DISCORD_API_TOKEN")
BASE_DIR=pathlib.Path(__file__).parent
CMDS_DIR=BASE_DIR / "cmds"
COGS_DIR=BASE_DIR / "cogs"
