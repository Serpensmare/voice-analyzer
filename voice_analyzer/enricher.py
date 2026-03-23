"""
Enrich transcription with AI-powered summary, key takeaways, action items, and speaker analysis.
Uses local Ollama (llama3.2) — zero API cost.
"""
import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def enrich(transcript_text: str, language: str = "en") -> dict:
    """
    Takes raw transcript text, returns enriched analysis dict with:
    - summary, key_takeaways, action_items, speaker_analysis, topics, sentiment
    """
    lang_instruction = "Respond in Spanish." if language == "es" else "Respond in English."
    
    prompt = f"""You are an expert meeting/conversation analyst. Analyze this transcript and provide a structured analysis.

{lang_instruction}

TRANSCRIPT:
{transcript_text[:8000]}

Provide your analysis in this exact JSON format (no markdown, just raw JSON):
{{
  "summary": "2-3 paragraph executive summary of the conversation",
  "key_takeaways": ["takeaway 1", "takeaway 2", "takeaway 3"],
  "action_items": ["action 1", "action 2", "action 3"],
  "decisions_made": ["decision 1", "decision 2"],
  "topics_discussed": ["topic 1", "topic 2", "topic 3"],
  "sentiment": "positive/negative/neutral/mixed",
  "speaker_analysis": "Brief analysis of each speaker's role and contributions",
  "follow_up_questions": ["question 1", "question 2"]
}}

Return ONLY valid JSON, nothing else."""

    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 2000}
    }).encode()

    req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            result = json.load(r)
            response_text = result.get("response", "")
            
            # Try to parse as JSON
            try:
                # Find JSON block in response
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                if start >= 0 and end > start:
                    return json.loads(response_text[start:end])
            except json.JSONDecodeError:
                pass
            
            # Fallback: return raw text as summary
            return {
                "summary": response_text,
                "key_takeaways": [],
                "action_items": [],
                "decisions_made": [],
                "topics_discussed": [],
                "sentiment": "unknown",
                "speaker_analysis": "",
                "follow_up_questions": []
            }
    except Exception as e:
        return {"summary": f"Enrichment failed: {e}", "key_takeaways": [], "action_items": []}
