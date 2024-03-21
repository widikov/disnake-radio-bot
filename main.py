import discord
from discord import FFmpegOpusAudio, FFmpegPCMAudio, PCMVolumeTransformer
from discord import Intents, Status
from discord.ext.commands import Bot
import os
import asyncio

SOURCE = ""
player = None
DEFAULT_VOLUME = 0.3

intents = Intents.default()
intents.members = True
intents.message_content = True

client = Bot(command_prefix=PREFIX, intents=intents)
TOKEN = "TOKEN" # change this for your bot token
PREFIX = "?" # change this for your bot prefix

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(
      type=discord.ActivityType.streaming,
      name="?play",
      url="https://www.youtube.com/watch?v=wK3U-TvX7yE"))

    
async def do_play(ctx, src):
    global player
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        await ctx.message.add_reaction('❌')
        return

    try:
        player = await channel.connect()
        await asyncio.sleep(5)
        await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
        await asyncio.sleep(3)
        player.play(PCMVolumeTransformer(FFmpegPCMAudio(src), volume=DEFAULT_VOLUME))
    except Exception:
        pass


class SelectorMenu(discord.ui.Select):

  def __init__(self, ctx, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.ctx = ctx

  async def callback(self, interaction: discord.Interaction):
    if self.values[0] == "radio2":
      SOURCE = "https://stream-160.zeno.fm/0r0xa792kwzuv?zs=M7mViwsrR46LNQGfLXSQGw"
    elif self.values[0] == "radio1":
      SOURCE = "https://stream-160.zeno.fm/0r0xa792kwzuv?zs=M7mViwsrR46LNQGfLXSQGw" # change the link of radio stream
    else:
      return

    await interaction.response.send_message(
        '✅ Success!', ephemeral=True)
    await do_play(self.ctx, SOURCE)

@client.command(aliases=['p', 'pla'])
async def play(ctx):
  select = SelectorMenu(
      ctx,
      custom_id="radio_selector",
      placeholder="Select a radio station",
      options=[
          discord.SelectOption(label="Radio 1",
                               value="radio1",
                               emoji="📻"),
          discord.SelectOption(label="Radio 2",
                               value="radio2",
                               emoji="📻"),
      ])

  embed = discord.Embed(title="Radio",
                        description="Select a radio station",
                        color=discord.Color.from_rgb(255, 209, 220)) # change embed color
  view = discord.ui.View()
  view.add_item(select)
  await asyncio.sleep(5)
  await ctx.send(embed=embed, view=view)


@client.command(aliases=['s', 'stp', 'leave', 'l'])
async def stop(ctx):
  if ctx.voice_client:
    ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    await ctx.message.add_reaction('✅')
  else:
    print("The player is not initialized.")


client.run(TOKEN)
