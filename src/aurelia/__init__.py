import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import asyncio
import time

from aurelia.cogs.liavc.vc import Vc

def main():
    pass

class Aurelia(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="", intents=intents)

    async def setup_hook(self) -> None:
        await self.add_cog(Vc(self))
    
bot = Aurelia()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Running as {bot.user}')

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot.run(BOT_TOKEN)
