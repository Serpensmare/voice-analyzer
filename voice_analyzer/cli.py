"""
voice-analyzer CLI
Usage: voice-analyzer analyze <audio_file> [--language es] [--enrich] [--push-crm]
"""
import click
import os
from .transcriber import transcribe
from .reporter import generate_report
from .enricher import enrich

@click.group()
def cli():
    """Voice Analyzer — transcribe + analyze + enrich audio, push to EspoCRM."""
    pass

@cli.command()
@click.argument("audio_file")
@click.option("--language", "-l", default="auto", help="Language code (es, en, auto)")
@click.option("--output", "-o", default=None, help="Output .analysis.md path")
@click.option("--push-crm", is_flag=True, help="Push result to EspoCRM")
@click.option("--crm-entity", default="Meeting", help="EspoCRM entity type")
@click.option("--enrich/--no-enrich", default=True, help="AI enrichment via local Ollama")
def analyze(audio_file, language, output, push_crm, crm_entity, enrich_flag):
    """Transcribe audio and generate enriched analysis report."""
    if not os.path.exists(audio_file):
        click.echo(f"Error: file not found: {audio_file}", err=True)
        raise SystemExit(1)

    click.echo(f"🎙️ Transcribing {audio_file}...")
    result = transcribe(audio_file, language=language)
    click.echo(f"📝 Detected language: {result['language']} | Duration: {result['duration']}s")

    enrichment = None
    if enrich_flag:
        click.echo(f"🧠 Enriching with local AI (llama3.2)...")
        enrichment = enrich(result["full_text"], language=result["language"])
        click.echo(f"✅ Enrichment complete")

    report_path = output or audio_file.replace(".ogg","").replace(".mp3","").replace(".m4a","").replace(".wav","") + ".analysis.md"
    report = generate_report(result, audio_file, enrichment=enrichment)

    with open(report_path, "w") as f:
        f.write(report)
    click.echo(f"📄 Report saved: {report_path}")

    if push_crm:
        from .crm import push_to_espocrm
        crm_id = push_to_espocrm(result, report, entity=crm_entity)
        click.echo(f"📋 Pushed to EspoCRM {crm_entity}: {crm_id}")

    click.echo("\n--- SUMMARY ---")
    if enrichment and enrichment.get("summary"):
        click.echo(enrichment["summary"][:500])
    else:
        click.echo(result["full_text"][:300])

    return result

if __name__ == "__main__":
    cli()
