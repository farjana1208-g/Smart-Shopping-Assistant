import os
import time
from dotenv import load_dotenv
from groq import Groq
from ddgs import DDGS

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def search_for_question(product_name, question):
    """Search DuckDuckGo for specific info about the product related to the question."""
    query = f"{product_name} {question}"
    results = []
    try:
        time.sleep(1)
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                results.append(r.get("body", ""))
    except Exception:
        pass
    return "\n".join(results)


def is_personal_recommendation(message):
    """Detect if the user is asking for a personalized recommendation."""
    keywords = [
        "should i", "is it good for me", "for student", "for gaming",
        "for photography", "for work", "my budget", "my needs",
        "recommend", "worth it for me", "suitable for", "fit for",
        "i am", "i'm a", "i need", "i want", "i use"
    ]
    lower = message.lower()
    return any(k in lower for k in keywords)


def chat_about_product(product_name, verdict, reviews, chat_history, user_message):
    """
    Chat with AI about the product.
    - Searches for specific info related to the question
    - Detects personal recommendation requests and tailors response
    """

    # search for specific info related to this question
    search_context = search_for_question(product_name, user_message)

    # build base context
    pros = ", ".join(verdict.get("pros", []))
    cons = ", ".join(verdict.get("cons", []))
    badge = verdict.get("badge", "UNKNOWN")
    rating = verdict.get("rating", 0)
    summary = verdict.get("summary", "")
    best_buy = verdict.get("best_place_to_buy", "")

    review_snippets = "\n".join(
        f"- {r.get('title','')}: {r.get('snippet','')}"
        for r in reviews if isinstance(r, dict)
    )

    # detect if personal recommendation needed
    if is_personal_recommendation(user_message):
        extra_instruction = """
The user seems to be asking for a personalized recommendation.
- Acknowledge their specific situation or needs
- Give a clear YES/NO/MAYBE recommendation tailored to them
- Explain briefly why it does or doesn't fit their needs
- Suggest an alternative if it's not a good fit for them
"""
    else:
        extra_instruction = """
- Answer the specific question directly and concisely
- Use the search results for specific details
- Be honest if information is not available
"""

    system_prompt = f"""You are a helpful shopping assistant. The user has analyzed the product "{product_name}".

Product Analysis:
- Verdict: {badge}
- Rating: {rating}/10
- Summary: {summary}
- Pros: {pros}
- Cons: {cons}
- Best place to buy: {best_buy}

Review snippets:
{review_snippets}

Fresh search results for this question:
{search_context}

Instructions:
{extra_instruction}

Keep your response under 4-5 sentences. Be friendly, direct and helpful."""

    messages = [{"role": "system", "content": system_prompt}]
    messages += chat_history
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.5,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I couldn't process that: {str(e)}"