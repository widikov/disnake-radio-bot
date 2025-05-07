# Discord Radio Bot

A simple Discord bot that allows users to play radio streams in voice channels using slash commands.

## Features

- Play radio streams in voice channels
- Select from multiple radio stations via a dropdown menu
- Stop playback and disconnect from voice channel
- Adjustable volume control (default: 30%)

## Setup

1. **Prerequisites**:
   - Python 3.8 or higher
   - FFmpeg installed and added to PATH
   - Disnake library (`pip install disnake`)
   - FFmpeg-Python (`pip install ffmpeg-python`)

2. **Configuration**:
   - Replace `TOKEN` in the code with your Discord bot token
   - Modify the `PREFIX` if you want a different command prefix
   - Add your radio stream URLs in the `SelectorMenu` class


## Commands

- `/play` - Open radio station selection menu
- `/stop` - Stop playback and leave voice channel

## Customization

- **Radio Stations**: Edit the options in the `SelectorMenu` class
- **Embed Color**: Change the RGB values in the `color` parameter
- **Default Volume**: Modify the `DEFAULT_VOLUME` variable (0.0 to 1.0)

## Troubleshooting

- If the bot fails to connect to voice, ensure:
- FFmpeg is properly installed
- The bot has permission to join voice channels
- The radio stream URLs are valid and accessible

## License

This project is open-source and available under the [MIT License](LICENSE).
