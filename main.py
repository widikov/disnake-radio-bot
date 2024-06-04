import disnake
from disnake import FFmpegPCMAudio, PCMVolumeTransformer
from disnake.ext import commands
import asyncio

SOURCE = ""
player = None
DEFAULT_VOLUME = 0.3

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

PREFIX = "?" # change this for your bot prefix
client = commands.Bot(command_prefix=PREFIX, intents=intents)
TOKEN = "TOKEN" # change this for your bot token

@client.event
async def on_ready():
    await client.change_presence(activity=disnake.Activity(
        type=disnake.ActivityType.streaming,
        name="?play",
        url="https://www.youtube.com/watch?v=wK3U-TvX7yE"))
    print(f'Logged in as {client.user}')

async def do_play(interaction: disnake.ApplicationCommandInteraction, src):
    global player
    try:
        channel = interaction.author.voice.channel
    except AttributeError:
        await interaction.followup.send('❌ You are not in a voice channel.', ephemeral=True)
        return

    try:
        player = await channel.connect()
        await asyncio.sleep(5)
        await interaction.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
        await asyncio.sleep(3)
        player.play(PCMVolumeTransformer(FFmpegPCMAudio(src), volume=DEFAULT_VOLUME))
        await interaction.followup.send('✅ Playing!', ephemeral=True)
    except Exception as e:
        print(e)
        await interaction.followup.send('❌ Failed to play.', ephemeral=True)

class SelectorMenu(disnake.ui.Select):
    def __init__(self, interaction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interaction = interaction

    async def callback(self, interaction: disnake.MessageInteraction):
        global SOURCE
        if self.values[0] == "radio2":
            SOURCE = "https://stream-160.zeno.fm/0r0xa792kwzuv?zs=M7mViwsrR46LNQGfLXSQGw"
        elif self.values[0] == "radio1":
            SOURCE = "https://stream-160.zeno.fm/0r0xa792kwzuv?zs=M7mViwsrR46LNQGfLXSQGw"  # change the link of radio stream
        else:
            return

        await self.interaction.followup.send('✅ Success!', ephemeral=True)
        await do_play(self.interaction, SOURCE)

@client.slash_command(name="play", description="Play a radio station")
async def play(interaction: disnake.ApplicationCommandInteraction):
    await interaction.response.defer(ephemeral=True)  # Defer the response to avoid timeout

    select = SelectorMenu(
        interaction,
        custom_id="radio_selector",
        placeholder="Select a radio station",
        options=[
            disnake.SelectOption(label="Radio 1",
                                 value="radio1",
                                 emoji="📻"),
            disnake.SelectOption(label="Radio 2",
                                 value="radio2",
                                 emoji="📻"),
        ])

    embed = disnake.Embed(title="Radio",
                          description="Select a radio station",
                          color=disnake.Color.from_rgb(255, 209, 220))  # change embed color
    view = disnake.ui.View()
    view.add_item(select)
    await asyncio.sleep(5)
    await interaction.followup.send(embed=embed, view=view)

@client.slash_command(name="stop", description="Stop the radio and leave the voice channel")
async def stop(interaction: disnake.ApplicationCommandInteraction):
    if interaction.guild.voice_client:
        interaction.guild.voice_client.stop()
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message('✅ Stopped and disconnected.', ephemeral=True)
    else:
        await interaction.response.send_message('❌ Not connected to a voice channel.', ephemeral=True)

client.run(TOKEN)
