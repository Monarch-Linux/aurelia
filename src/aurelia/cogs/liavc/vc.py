import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests
import os

class Vc(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    lia = app_commands.Group(name="liavc", description="Aurelia VC Commands")

    @lia.command(name="join", description="Make Aurelia join the VC you are currently in")
    async def _join(self, interaction: discord.Interaction):
        await interaction.response.send_message('Joining VC...', ephemeral=True)
        
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            vc = await channel.connect()

            await interaction.followup.send("Joined VC", ephemeral=True)
        else:
            await interaction.followup.send("You need to be in a voice channel to use this command!", ephemeral=True)

    @lia.command(name="leave", description="Make Aurelia leave the VC that it is currently in")
    async def _leave(self, interaction: discord.Interaction):
        await interaction.response.send_message('Leaving VC...', ephemeral=True)

        if interaction.guild.voice_client:
            channel = interaction.guild.voice_client
            vc = await channel.disconnect()

            await interaction.followup.send("Left VC", ephemeral=True)
        else:
            await interaction.followup.send("Aurelia needs to be in a voice channel to use this command.", ephemeral=True)

    @lia.command(name="playsound", description="Make Aurelia play a sound from a link")
    async def _playsound(self, interaction: discord.Interaction, url:str):
        await interaction.response.send_message('Playing sound...', ephemeral=True)

        if interaction.user.voice:
            channel = interaction.user.voice.channel
            vc = await channel.connect()
            
            response = requests.get(url)
            if response.status_code == 200:
                with open("audio.mp3", 'wb') as f:
                    f.write(response.content)
            else:
                print(f"Failed to download, HTTP Status code: {response.status_code}")

            discord.opus.load_opus("/usr/lib64/libopus.so")
            if not discord.opus.is_loaded():
                raise RunTimeError('Opus failed to load')

            vc.play(discord.FFmpegPCMAudio("audio.mp3"))

            while vc.is_playing():
                await asyncio.sleep(1)
            
            await vc.disconnect()
            os.remove("audio.mp3")
            
            await interaction.followup.send("Played.", ephemeral=True)
        else:
            await interaction.followup.send("You need to be in a voice channel to use this command!", ephemeral=True)

