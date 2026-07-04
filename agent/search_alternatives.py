import time
from ddgs import DDGS

def search_alternatives(product_name, max_results=5):
    query = f"{product_name} alternatives best competitors comparison"
    results = []
    try:
        time.sleep(3)
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", "")
                })
    except Exception as e:
        print(f"Alternatives search error: {e}")
    return results