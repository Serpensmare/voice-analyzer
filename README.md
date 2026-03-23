# 🎙️ Voice Analyzer

**Fully local** audio transcription + AI-powered analysis. Analyze any voice recording — meeting recordings, voice memos, interviews, podcasts, phone calls, lectures. Not just Telegram voice notes. Zero API costs. Runs on a Raspberry Pi, Mac Mini, or any machine with Python.

> **Use case:** You just had an important 45-minute meeting. Complex topics, fast decisions, action items flying around. Instead of taking notes — just record it. Drop the audio into Voice Analyzer and get back a full executive summary, key takeaways, KPIs, action items, and a timestamped transcript. All processed locally on your hardware. No data leaves your machine.

## Works great with

- 🦞 **[OpenClaw](https://openclaw.ai)** — run it as an always-on Telegram bot alongside your AI assistant
- 🖥️ **Mac Mini / MacBook** — use the CLI to analyze recordings from your desk
- 🍓 **Raspberry Pi** — lightweight enough to run 24/7 on a Pi 4/5
- 🐧 **Any Linux machine** — just needs Python + Ollama

## What it does

```
Any Audio File → faster-whisper (local STT) → Ollama llama3.2 (local AI) → Rich Analysis Report
```

**Pipeline:**
1. 🎙️ **Transcribe** — Local speech-to-text via [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (runs on CPU, no GPU needed)
2. 🧠 **Enrich** — AI analysis via [Ollama](https://ollama.ai) (llama3.2) generates:
   - Executive summary
   - Key takeaways & KPIs
   - Action items with owners
   - Decisions made
   - Topics discussed
   - Sentiment analysis
   - Follow-up questions
3. 📄 **Report** — Beautiful `.analysis.md` markdown report
4. 📱 **Telegram Bot** — Send voice notes, get analysis back instantly

**💰 Total cost: $0** — everything runs locally on your hardware.

## Why use this?

| Scenario | Without Voice Analyzer | With Voice Analyzer |
|----------|----------------------|---------------------|
| 45-min strategy meeting | Scramble to take notes, miss half the details | Record → full summary + action items in 2 min |
| Quick voice memo with ideas | Forget what you said by tomorrow | Transcribed, enriched, searchable forever |
| Client call with decisions | "Wait, what did we agree on?" | Clear decisions list + follow-up items |
| Brainstorming session | Ideas lost in the chaos | Every idea captured, categorized, prioritized |

## Requirements

- Python 3.10+
- [Ollama](https://ollama.ai) with `llama3.2` model pulled
- ffmpeg
- A Telegram bot token (from [@BotFather](https://t.me/BotFather)) — for the bot mode

## Quick Start

```bash
# Clone
git clone https://github.com/Serpensmare/voice-analyzer.git
cd voice-analyzer

# Install
python3 -m venv .venv
source .venv/bin/activate
pip install faster-whisper python-telegram-bot requests click

# Pull the AI model
ollama pull llama3.2

# Analyze an audio file
voice-analyzer analyze recording.m4a
```

## Telegram Bot Mode

```bash
# Set environment
export TELEGRAM_BOT_TOKEN="your-bot-token"
export ALLOWED_CHAT_ID="your-telegram-chat-id"  # optional
export VOICE_LANGUAGE="auto"  # or "es", "en", etc.

# Run the bot
python3 bot.py
```

Send a voice note → get back a full enriched analysis. That's it.

## CLI Usage

```bash
# Basic transcription + enrichment
voice-analyzer analyze audio.ogg

# Specify language
voice-analyzer analyze meeting.m4a --language es

# Skip AI enrichment (transcription only)
voice-analyzer analyze audio.ogg --no-enrich

```

## OpenClaw Integration

If you're running [OpenClaw](https://openclaw.ai), set up Voice Analyzer as a systemd service:

```ini
[Unit]
Description=Voice Analyzer Telegram Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/voice-analyzer
Environment=TELEGRAM_BOT_TOKEN=your-token
Environment=VOICE_LANGUAGE=auto
ExecStart=/path/to/voice-analyzer/.venv/bin/python3 bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

It runs alongside your OpenClaw agent — voice notes get transcribed and enriched automatically while your agent handles everything else.

## Output Example

The analyzer generates a `.analysis.md` file:

```markdown
# Voice Analysis — meeting-2024-03-15.m4a

**Date:** 2024-03-15 14:30
**Duration:** 45m 12s
**Language:** EN
**Model:** faster-whisper (local) + llama3.2 (local)

## Summary
The meeting covered three main topics: Q1 revenue performance,
the upcoming product launch timeline, and hiring priorities...

## Key Takeaways
- Q1 revenue exceeded targets by 12%
- Product launch moved to April 15
- Need to hire 2 senior engineers by end of month

## Action Items
- [ ] Send updated timeline to stakeholders
- [ ] Post job listings for senior engineers
- [ ] Schedule follow-up review for April 1

## Decisions Made
- Launch date confirmed: April 15
- Budget approved for contractor support

## Transcript
[00:00] Welcome everyone, let's get started...
[00:15] First, let's look at Q1 numbers...
```



```bash
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Any Audio   │────▶│ faster-whisper│────▶│  Ollama     │
│  File        │     │  (local STT) │     │  llama3.2   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                 │
                    ┌──────────────┐     ┌───────▼──────┐
                    │  (optional)  │     │  report      │
                    └──────────────┘     └──────────────┘
```

## Supported Audio Formats

- `.ogg` (Telegram voice notes)
- `.m4a` / `.mp4` (iPhone recordings, meetings)
- `.mp3`
- `.wav`
- Any format supported by ffmpeg

## License

MIT

---

Built with 🦞 [OpenClaw](https://openclaw.ai)
