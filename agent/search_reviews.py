import time
from ddgs import DDGS

def search_product_reviews(product_name, max_results=5):
    query = f"{product_name} review worth buying"
    results = []
    try:
        time.sleep(1)
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", ""),
                    "url": r.get("href", "")
                })
    except Exception as e:
        print(f"Review search error: {e}")
    return results