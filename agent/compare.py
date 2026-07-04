import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def compare_products(product1, verdict1, product2, verdict2):
    """
    Compare two products and return a recommendation.
    """
    prompt = f"""Compare these two products and give a clear recommendation.

Product 1: {product1}
- Badge: {verdict1.get('badge')}
- Rating: {verdict1.get('rating')}/10
- Pros: {', '.join(verdict1.get('pros', []))}
- Cons: {', '.join(verdict1.get('cons', []))}
- Summary: {verdict1.get('summary')}

Product 2: {product2}
- Badge: {verdict2.get('badge')}
- Rating: {verdict2.get('rating')}/10
- Pros: {', '.join(verdict2.get('pros', []))}
- Cons: {', '.join(verdict2.get('cons', []))}
- Summary: {verdict2.get('summary')}

Return ONLY a JSON object with these exact keys:
- "winner": the name of the better product (exactly as given above)
- "reason": 2-3 sentences explaining why it wins
- "product1_score": a score out of 10 for {product1}
- "product2_score": a score out of 10 for {product2}
- "best_for_budget": which is better for budget buyers and why (one sentence)
- "best_for_quality": which is better for quality seekers and why (one sentence)

Return ONLY valid JSON, no markdown, no extra text."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
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
            "winner": "Unknown",
            "reason": f"Could not compare: {str(e)}",
            "product1_score": 0,
            "product2_score": 0,
            "best_for_budget": "No data",
            "best_for_quality": "No data"
        }