"""
Persona detection: classifies the user's message into one of three
personas so the response generator can adapt tone and depth.
"""
import config
import llm_client

_VALID_PERSONAS = set(config.PERSONAS)

SYSTEM_INSTRUCTION = (
    "You classify customer support messages into exactly one persona. "
    "Respond with ONLY the persona name, nothing else — no punctuation, "
    "no explanation."
)

PROMPT_TEMPLATE = """Classify the user's message into exactly one of these personas:

1. Technical Expert — uses technical terms, asks about logs/APIs/root cause/error codes, wants precise detail
2. Frustrated User — expresses annoyance, repeats failed attempts, uses emotional language, wants empathy and simple steps
3. Business Executive — focused on business impact, cost, timelines, SLAs, asks "how does this affect us"

Message:
\"\"\"{message}\"\"\"

Respond with only one of: Technical Expert, Frustrated User, Business Executive
"""


def detect_persona(message):
    """
    Returns one of config.PERSONAS. Falls back to "Frustrated User"
    (the safest default — empathetic, simple language) if the LLM
    returns something unparseable, rather than crashing the pipeline.
    """
    prompt = PROMPT_TEMPLATE.format(message=message)

    try:
        raw = llm_client.generate(prompt, system_instruction=SYSTEM_INSTRUCTION, temperature=0)
    except RuntimeError:
        raise
    except Exception:
        return "Frustrated User"

    cleaned = raw.strip().strip(".").strip()

    if cleaned in _VALID_PERSONAS:
        return cleaned

    
    for persona in _VALID_PERSONAS:
        if persona.lower() in cleaned.lower():
            return persona

    return "Frustrated User"


if __name__ == "__main__":
    import sys
    msg = sys.argv[1] if len(sys.argv) > 1 else "Can you provide API logs for the 401 errors?"
    print(detect_persona(msg))
