"""
Generate .analysis.md report from transcription + enrichment.
"""
import datetime
import os

def generate_report(result: dict, audio_file: str, enrichment: dict = None) -> str:
    segments = result["segments"]
    duration = result["duration"]
    language = result["language"]
    full_text = result["full_text"]
    word_count = len(full_text.split())

    mins = int(duration // 60)
    secs = int(duration % 60)
    duration_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"

    lines = [
        f"# Voice Analysis — {os.path.basename(audio_file)}",
        f"",
        f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Language:** {language.upper()}  ",
        f"**Duration:** {duration_str}  ",
        f"**Words:** {word_count}  ",
        f"**Model:** faster-whisper (local) + llama3.2 (local)  ",
        f"",
        f"---",
        f"",
    ]

    # Add enrichment if available
    if enrichment and enrichment.get("summary"):
        lines += [
            f"## Summary",
            f"",
            enrichment.get("summary", ""),
            f"",
        ]

        takeaways = enrichment.get("key_takeaways", [])
        if takeaways:
            lines += [f"## Key Takeaways", f""]
            for t in takeaways:
                lines.append(f"- {t}")
            lines.append("")

        actions = enrichment.get("action_items", [])
        if actions:
            lines += [f"## Action Items", f""]
            for a in actions:
                lines.append(f"- [ ] {a}")
            lines.append("")

        decisions = enrichment.get("decisions_made", [])
        if decisions:
            lines += [f"## Decisions Made", f""]
            for d in decisions:
                lines.append(f"- {d}")
            lines.append("")

        topics = enrichment.get("topics_discussed", [])
        if topics:
            lines += [f"## Topics Discussed", f""]
            for t in topics:
                lines.append(f"- {t}")
            lines.append("")

        sentiment = enrichment.get("sentiment", "")
        if sentiment:
            lines += [f"## Sentiment: {sentiment}", f""]

        speaker = enrichment.get("speaker_analysis", "")
        if speaker:
            lines += [f"## Speaker Analysis", f"", speaker, f""]

        follow_up = enrichment.get("follow_up_questions", [])
        if follow_up:
            lines += [f"## Follow-Up Questions", f""]
            for q in follow_up:
                lines.append(f"- {q}")
            lines.append("")

    # Transcript
    lines += [
        f"---",
        f"",
        f"## Transcript",
        f"",
    ]

    for seg in segments:
        mins_s = int(seg["start"] // 60)
        secs_s = int(seg["start"] % 60)
        timestamp = f"[{mins_s:02d}:{secs_s:02d}]"
        lines.append(f"{timestamp} {seg['text']}")

    lines += [
        f"",
        f"---",
        f"",
        f"## Full Text",
        f"",
        full_text,
    ]

    return "\n".join(lines)
