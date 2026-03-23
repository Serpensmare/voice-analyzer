#!/usr/bin/env python3
"""
Telegram → Voice Analyzer → AI Enrichment → EspoCRM bot.
Fully local: faster-whisper + Ollama (llama3.2) + EspoCRM.
Zero API costs. Everything runs on your hardware.
"""
import os, sys, tempfile, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

sys.path.insert(0, os.path.dirname(__file__))
from voice_analyzer.transcriber import transcribe
from voice_analyzer.reporter import generate_report
from voice_analyzer.enricher import enrich
from voice_analyzer.crm import push_to_espocrm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ALLOWED_CHAT_ID = int(os.environ.get("ALLOWED_CHAT_ID", "0"))
LANGUAGE = os.environ.get("VOICE_LANGUAGE", "auto")
CRM_ENTITY = os.environ.get("CRM_ENTITY", "Meeting")
ENABLE_CRM = os.environ.get("ENABLE_CRM", "false").lower() == "true"

async def handle_voice(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if ALLOWED_CHAT_ID and chat_id != ALLOWED_CHAT_ID:
        return

    msg = update.message
    voice = msg.voice or msg.audio or msg.document
    if not voice:
        return

    await msg.reply_text("🎙️ Transcribing...")

    file = await ctx.bot.get_file(voice.file_id)
    suffix = ".ogg"
    if hasattr(voice, "mime_type") and voice.mime_type:
        if "mp4" in voice.mime_type or "m4a" in voice.mime_type: suffix = ".m4a"
        elif "mpeg" in voice.mime_type or "mp3" in voice.mime_type: suffix = ".mp3"

    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        audio_path = tmp.name
    await file.download_to_drive(audio_path)

    try:
        result = transcribe(audio_path, language=LANGUAGE)
        log.info(f"Transcribed: {len(result['segments'])} segments, {result['duration']}s")

        await msg.reply_text("🧠 Analyzing with local AI...")
        enrichment = enrich(result["full_text"], language=result["language"])

        report = generate_report(result, audio_path, enrichment=enrichment)
        report_path = audio_path + ".analysis.md"
        with open(report_path, "w") as f:
            f.write(report)

        crm_id = None
        if ENABLE_CRM:
            crm_id = push_to_espocrm(result, report, entity=CRM_ENTITY)

        dur = result["duration"]
        mins, secs = int(dur // 60), int(dur % 60)
        dur_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"

        summary = enrichment.get("summary", result["full_text"][:300])[:400]
        takeaways = enrichment.get("key_takeaways", [])
        actions = enrichment.get("action_items", [])

        reply = f"✅ *Analyzed*\n\n"
        reply += f"🕐 {dur_str} | 🌐 {result['language'].upper()}\n"
        if crm_id:
            reply += f"📋 CRM: `{crm_id}`\n"
        reply += f"\n*Summary:*\n{summary}\n"

        if takeaways:
            reply += f"\n*Key Takeaways:*\n"
            for t in takeaways[:5]:
                reply += f"• {t}\n"

        if actions:
            reply += f"\n*Action Items:*\n"
            for a in actions[:5]:
                reply += f"☐ {a}\n"

        await msg.reply_text(reply, parse_mode="Markdown")

    except Exception as e:
        log.error(f"Error: {e}", exc_info=True)
        await msg.reply_text(f"❌ Error: {str(e)[:200]}")
    finally:
        os.unlink(audio_path)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_voice))
    log.info("Voice Analyzer Bot started — fully local enrichment mode")
    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
