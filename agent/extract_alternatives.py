import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def suggest_alternatives(product_name, alt_results):
    if not alt_results:
        return []

    lines = []
    for item in alt_results:
        try:
            if isinstance(item, dict):
                lines.append(
                    f"Title: {item.get('title','')}\n"
                    f"Snippet: {item.get('snippet','')}"
                )
            else:
                lines.append(str(item))
        except Exception:
            lines.append(str(item))

    snippets_text = "\n\n".join(lines)

    prompt = f"""Based on the search results about alternatives to "{product_name}", extract up to 4 specific alternative product names.

Output a JSON array of objects with these exact keys:
- "name": specific product name (e.g. "Redmi Note 14 Pro")
- "reason": one short sentence (max 15 words) why someone might prefer it

Only include real specific products mentioned in the text. Return ONLY valid JSON, no markdown, no extra text.

Search results:
{snippets_text}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.strip("`")
            if raw.lower().startswith("json"):
                raw = raw[4:].strip()

        parsed = json.loads(raw)
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []