# Groove Deck 🎵

A self-hosted Discord music bot built with Python that provides reliable music playback with queue management features.

## Features

- **Music Playback**: Play songs from YouTube using `/play`
- **Queue Management**: View, skip, stop, remove, and reorder tracks
- **Slash Commands**: Modern Discord slash command interface
- **Multi-Server Support**: Handles multiple Discord servers independently
- **Secure**: Minimal permissions, channel whitelisting, environment-based configuration

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/play` | Play a song from YouTube | `/play query:song name or artist` |
| `/queue` | Show current queue and now playing | `/queue` |
| `/skip` | Skip current song | `/skip` |
| `/stop` | Stop playback and clear queue | `/stop` |
| `/remove` | Remove song from queue | `/remove position:1` |
| `/move` | Move song to different position | `/move from_position:1 to_position:3` |

## Requirements

- **Python**: 3.11 or higher
- **FFmpeg**: For audio processing
- **Discord Bot Token**: From Discord Developer Portal
- **MiniConda**: For environment management (recommended)

## Setup

### 1. Environment Setup

Create and activate a new MiniConda environment:

```bash
conda create --name groove-deck python=3.11 -y
conda activate groove-deck
```

### 2. Install Dependencies

Install Python packages:

```bash
pip install -r requirements.txt
```

Install FFmpeg (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install ffmpeg
```

Install FFmpeg (macOS with Homebrew):

```bash
brew install ffmpeg
```

### 3. Discord Bot Configuration

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section and click "Add Bot"
4. Copy the bot token
5. **Important**: Enable Privileged Gateway Intents:
   - In the Bot section, scroll down to "Privileged Gateway Intents"
   - Enable **Message Content Intent**
   - Enable **Server Members Intent** (if you plan to use user mentions)
   - Enable **Presence Intent** (if you plan to use presence updates)
6. Go to "OAuth2" → "URL Generator"
7. Select scopes: `bot` and `applications.commands`
8. Select bot permissions:
   - `Send Messages`
   - `Use Slash Commands`
   - `Connect`
   - `Speak`
   - `Use Voice Activity`
9. Copy the generated URL and invite the bot to your server

### 4. Environment Configuration

Copy the example environment file:

```bash
cp env.example .env
```

Edit `.env` with your configuration:

```env
# Discord Bot Token
DISCORD_TOKEN=your_discord_bot_token_here

# Channel Whitelist (comma-separated channel IDs)
ALLOWED_CHANNEL_IDS=1234567890123456,2345678901234567

# Bot Configuration
BOT_PREFIX=!
LOG_LEVEL=INFO
```

**Important**: Replace `ALLOWED_CHANNEL_IDS` with the actual channel IDs where you want the bot to work. You can get channel IDs by enabling Developer Mode in Discord and right-clicking on channels.

### 5. Run the Bot

**Option 1: Full Features (Recommended)**
```bash
python main.py
```

**Option 2: Minimal Intents (If you can't enable privileged intents)**
```bash
python src/bot_minimal.py
```

The bot will connect to Discord and register slash commands. You should see confirmation messages in the console.

**Note**: If you get a "privileged intents" error, you have two choices:
1. **Enable privileged intents** in Discord Developer Portal (recommended for full features)
2. **Use the minimal bot** (`python src/bot_minimal.py`) which works without privileged intents

## Usage

### Basic Music Playback

1. Join a voice channel in your Discord server
2. Use `/play query:song name` to search and play music
3. The bot will join your voice channel and start playing

### Queue Management

- Use `/queue` to see what's currently playing and what's next
- Use `/skip` to skip the current song
- Use `/stop` to stop playback and clear the queue
- Use `/remove position:1` to remove a specific track
- Use `/move from_position:1 to_position:3` to reorder tracks

## Project Structure

```
groove-deck/
├── src/
│   ├── commands/          # Slash command implementations
│   │   ├── play.py        # Play command
│   │   └── queue.py       # Queue management commands
│   ├── services/          # Core services
│   │   ├── audio_player.py # Audio playback and queue management
│   │   └── youtube_service.py # YouTube integration
│   ├── bot.py             # Main bot class
│   ├── config.py          # Configuration management
│   └── logger.py          # Logging setup
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
├── env.example           # Environment configuration template
└── README.md             # This file
```

## Development

### Adding New Commands

1. Create a new file in `src/commands/`
2. Inherit from `commands.Cog`
3. Use `@app_commands.command` decorator for slash commands
4. Add the command to `bot.py` setup_hook method

### Testing

The bot includes comprehensive error handling and logging. Check the console output for debugging information.

## Troubleshooting

### Common Issues

1. **Bot doesn't respond to commands**
   - Check if the bot has the required permissions
   - Verify the channel is in `ALLOWED_CHANNEL_IDS`
   - Ensure slash commands are synced

2. **Audio doesn't play**
   - Verify FFmpeg is installed and accessible
   - Check if the bot has permission to join voice channels
   - Ensure the bot has permission to speak in voice channels

3. **Import errors**
   - Make sure you're in the correct conda environment
   - Verify all dependencies are installed with `pip install -r requirements.txt`

4. **Privileged Intents Error**
   - Error: "Shard ID None is requesting privileged intents that have not been explicitly enabled"
   - **Solution**: Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Select your bot application → Bot section
   - Scroll down to "Privileged Gateway Intents"
   - Enable **Message Content Intent** and **Server Members Intent**
   - Restart your bot

### Logs

The bot logs all activities to the console. Set `LOG_LEVEL=DEBUG` in your `.env` file for more detailed information.

## Security Features

- **Minimal Permissions**: Bot only requests necessary permissions
- **Channel Whitelisting**: Commands only work in specified channels
- **Environment Variables**: Sensitive data stored in `.env` file
- **Input Validation**: All user inputs are validated and sanitized

## Future Enhancements

- Spotify integration for better search results
- Audio caching for improved performance
- Web dashboard for queue control
- Advanced queue features (loop, shuffle)
- Support for additional platforms (SoundCloud, Bandcamp)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the console logs for error messages
3. Ensure your configuration is correct
4. Open an issue on GitHub with detailed information