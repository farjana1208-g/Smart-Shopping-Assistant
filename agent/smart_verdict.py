import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_verdict(product_name, reviews):
    if not reviews:
        return {
            "badge": "UNKNOWN",
            "rating": 0,
            "summary": "Not enough review data found.",
            "pros": [],
            "cons": [],
            "best_place_to_buy": "No data available"
        }

    parts = []
    for item in reviews:
        try:
            if isinstance(item, dict):
                parts.append(str(item.get("title", "")) + ": " + str(item.get("snippet", "")))
            else:
                parts.append(str(item))
        except Exception:
            parts.append(str(item))

    review_text = "\n\n".join(parts)

    prompt = f"""Based on these reviews about {product_name}, return ONLY a JSON object with keys: badge (BUY/AVOID/WAIT FOR SALE), rating (1-10), summary (2-3 sentences), pros (list of 3-4 short phrases), cons (list of 2-3 short phrases), best_place_to_buy (one sentence). No markdown, no extra text.

Reviews:
{review_text}"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=600
        )

        raw = response.choices[0].message.content.strip()
        raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
        raw = re.sub(r'```\s*$', '', raw, flags=re.MULTILINE)
        raw = raw.strip()
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            raw = match.group(0)

        return json.loads(raw)

    except Exception as e:
        return {
            "badge": "UNKNOWN",
            "rating": 0,
            "summary": f"Could not generate verdict: {str(e)}",
            "pros": [],
            "cons": [],
            "best_place_to_buy": "No data available"
        }