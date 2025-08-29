# Discord Music Bot Project Plan and Requirements

## 1. Project Overview
Build a self-hosted, Python-based Discord music bot with minimal permissions and slash command support. The bot will:
- Play songs in voice channels.
- Search Spotify for matches.
- Validate availability on YouTube.
- Stream audio with `yt-dlp` + `ffmpeg`.
- Provide queue management features.

## 2. Goals

- **Minimal & Secure**
  - No admin permissions.
  - Only respond in whitelisted channels.
  - Tokens stored securely.

- **Basic, Reliable Features**
  - `/play` to queue music.
  - `/queue` to show what’s playing and what’s next.
  - `/skip`, `/stop`, `/remove`, `/move` for control.

- **User-Friendly**
  - Interactive menus for track selection.
  - Clear embeds for feedback and queue info.

## 3. Tech Stack

| Component | Choice | Reason |
|------------|--------|--------|
| Discord Library | `discord.py` 2.x | Actively maintained, supports slash commands & voice |
| YouTube Playback | `yt-dlp` | Reliable, frequently updated |
| Audio Streaming | `ffmpeg` | Standard for voice streaming |
| Spotify Search | Spotify Web API | Provides metadata and search accuracy |
| Hosting | VPS or local container | Lightweight self-hosting |

## 4. Core Features

### Commands

| Command | Description |
|----------|-------------|
| `/play [song] [artist]` | Search Spotify, present top matches, validate with YouTube, queue the song, and start playback if idle |
| `/queue` | Display current song and queue list |
| `/skip` | Skip the current song and move to the next |
| `/stop` | Stop playback, clear queue, and disconnect from voice channel |
| `/remove [position]` | Remove a song from the queue |
| `/move [from] [to]` | Reorder queue items |

## 5. Requirements

### Functional
- Join the user’s voice channel when playback starts.
- Maintain per-guild queues to handle multiple servers.
- Auto-play next track in queue.
- Provide error messages for invalid requests (e.g., no voice channel, invalid song, etc.).
- Respond only in whitelisted text channels.

### Non-Functional
- Tokens (Discord, Spotify) must be stored securely in `.env`.
- Code should be modular and easy to maintain.
- Logging for debugging and error tracking.
- Unit-testable for core logic (queue management, Spotify/YouTube lookup).

## 6. Permissions

Minimal OAuth scope:
- `applications.commands`
- `connect`
- `speak`

## 7. High-Level Architecture

```
src/
├─ bot.py               # Entry point
├─ commands/
│  ├─ play.py           # /play implementation
│  ├─ queue.py          # /queue, /remove, /move, /skip, /stop
├─ services/
│  ├─ spotify_service.py # Spotify API interaction
│  ├─ youtube_service.py # yt-dlp integration
│  ├─ audio_player.py    # Queue + playback controller
├─ utils/
│  ├─ config.py          # Environment handling
│  ├─ logger.py          # Logging setup
.env.example
requirements.txt
README.md
```

## 8. Development Plan

### Phase 1 – Setup & Core Playback
- Initialize project, virtual environment, and `.env` handling.
- Install core dependencies:
  ```bash
  pip install discord.py yt-dlp python-dotenv requests
  sudo apt install ffmpeg
  ```
- Create bot entry point (`bot.py`) that connects and registers slash commands.
- Implement basic `/play` with hardcoded YouTube URL streaming to VC.

### Phase 2 – Spotify + YouTube Integration
- Set up Spotify API credentials and simple search.
- Filter results to playable YouTube matches using `yt-dlp`.
- Return options as an interactive menu for the user to pick.

### Phase 3 – Queue & Playback Logic
- Implement per-guild queue handling.
- Add `/queue`, `/skip`, `/stop`.
- Implement auto-play of next track when one ends.

### Phase 4 – Queue Management
- Add `/remove` and `/move` commands.
- Add feedback messages for each operation.

### Phase 5 – Polishing
- Embed-based feedback for now-playing, queue list.
- Channel whitelist enforcement.
- Logging and error handling.
- Unit tests for queue logic and service layers.

## 9. Environment Variables

`.env.example`:
```env
DISCORD_TOKEN=your_discord_bot_token
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
ALLOWED_CHANNEL_IDS=1234567890123456,2345678901234567
```

## 10. Testing Plan

- **Unit Tests**:
  - Queue behavior: adding, removing, reordering.
  - Spotify search parsing.
- **Integration Tests**:
  - End-to-end command flow in a test server.
- **Manual Tests**:
  - Join voice channel, play, skip, stop, queue.

## 11. Deployment

- Host on Linux VPS or Docker container:
  - Python 3.11+
  - `ffmpeg` installed
- Use `systemd` or `pm2` for process management.
- Automate deployment with a GitHub Actions workflow.

## 12. Future Enhancements
- Add caching for frequently played tracks.
- Optional support for SoundCloud or Bandcamp.
- Advanced queue features (loop, shuffle).
- Web dashboard for queue control.

