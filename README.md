# 🎙️ Voice Analyzer

**Fully local** voice memo transcription + AI-powered analysis pipeline. Zero API costs. Runs on a Raspberry Pi.

Send a voice note on Telegram → get back a full analysis with summary, key takeaways, action items, and more.

## What it does

```
Voice Note → faster-whisper (local STT) → Ollama llama3.2 (local AI) → Rich Analysis Report
```

**Features:**
- 🎙️ Local transcription via [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (Whisper on CPU)
- 🧠 AI enrichment via [Ollama](https://ollama.ai) (llama3.2) — summary, takeaways, action items, sentiment
- 📱 Telegram bot — send voice notes, get analysis back
- 📋 Optional EspoCRM integration — auto-save meetings/notes
- 📄 Markdown reports (`.analysis.md`)
- 💰 **$0 cost** — everything runs locally

## Requirements

- Python 3.10+
- [Ollama](https://ollama.ai) with `llama3.2` model pulled
- ffmpeg
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/voice-analyzer.git
cd voice-analyzer

# Install
python3 -m venv .venv
source .venv/bin/activate
pip install faster-whisper python-telegram-bot requests click

# Pull the AI model
ollama pull llama3.2

# Set environment
export TELEGRAM_BOT_TOKEN="your-bot-token"
export ALLOWED_CHAT_ID="your-telegram-chat-id"  # optional
export VOICE_LANGUAGE="auto"  # or "es", "en", etc.

# Run the bot
python3 bot.py
```

## CLI Usage

```bash
# Basic transcription + enrichment
.venv/bin/voice-analyzer analyze audio.ogg

# Specify language
.venv/bin/voice-analyzer analyze meeting.m4a --language es

# Skip AI enrichment (transcription only)
.venv/bin/voice-analyzer analyze audio.ogg --no-enrich

# Push to EspoCRM
export ESPO_BASE="http://localhost:8080/api/v1"
export ESPO_USER="admin"
export ESPO_PASS="your-password"
.venv/bin/voice-analyzer analyze audio.ogg --push-crm
```

## Output Example

The analyzer generates a `.analysis.md` file with:

- **Summary** — 2-3 paragraph executive summary
- **Key Takeaways** — bullet points of main insights
- **Action Items** — checkboxes for follow-ups
- **Decisions Made** — what was decided
- **Topics Discussed** — main themes
- **Sentiment** — overall tone
- **Full Transcript** — timestamped

## EspoCRM Integration (Optional)

Set these environment variables to auto-push analyses to EspoCRM:

```bash
export ENABLE_CRM="true"
export ESPO_BASE="http://localhost:8080/api/v1"
export ESPO_USER="admin"
export ESPO_PASS="your-password"
export CRM_ENTITY="Meeting"  # or "Note"
```

## Systemd Service

```ini
[Unit]
Description=Voice Analyzer Telegram Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/voice-analyzer
Environment=TELEGRAM_BOT_TOKEN=your-token
Environment=VOICE_LANGUAGE=es
ExecStart=/path/to/voice-analyzer/.venv/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Telegram    │────▶│ faster-whisper│────▶│  Ollama     │
│  Voice Note  │     │  (local STT) │     │  llama3.2   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                 │
                    ┌──────────────┐     ┌───────▼──────┐
                    │  EspoCRM     │◀────│  .analysis.md│
                    │  (optional)  │     │  report      │
                    └──────────────┘     └──────────────┘
```

## License

MIT
