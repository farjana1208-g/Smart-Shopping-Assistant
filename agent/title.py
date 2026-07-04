import re
from collections import defaultdict

GENERIC_WORDS = {
    "search", "mobile", "smartphone", "phone", "5g", "4g", "lte",
    "new", "launch", "sale", "best", "buy", "offer", "deal",
    "discount", "limited", "edition", "fastest", "biggest", "brightest",
    "segment", "resistance", "rating", "reviews", "stable", "gaming",
    "battery", "display", "charging", "processor", "chipset", "performance",
    "powered", "trust", "shipping", "selected", "color", "variant", "now",
    "with", "from", "hrs", "nits", "hz", "mah", "upto", "and",
    "visit", "store", "amazon", "flipkart", "choice", "bought",
    "past", "month", "off", "home", "you", "wallet", "cart",
    "menu", "world", "budget", "leading", "snap", "power",
    "genuine", "original", "official", "certified", "premium"
}

SPEC_TOKENS = {
    "gb", "tb", "ram", "rom", "mp", "mah", "inch", "watt",
    "₹", "$", "%", "price", "emi", "antutu", "score", "nits", "hz",
    "fhd", "uhd", "amoled", "oled", "ip64", "ip68", "ip69",
    "rpm", "kg", "lbs", "ml", "litre", "liter", "mm", "cm"
}

KNOWN_BRANDS = [
    # phones
    "motorola", "moto", "samsung", "redmi", "xiaomi", "realme",
    "oppo", "oneplus", "vivo", "apple", "iphone", "nokia", "asus",
    "poco", "infinix", "tecno", "lava", "google", "pixel", "honor",
    "lenovo", "nothing", "iqoo", "micromax", "huawei",

    # laptops
    "dell", "hp", "acer", "asus", "msi", "razer", "surface",
    "thinkpad", "ideapad", "inspiron", "pavilion", "envy", "spectre",
    "macbook", "chromebook", "zenbook", "vivobook", "predator",

    # audio
    "sony", "bose", "jbl", "sennheiser", "boat", "boult", "noise",
    "oneodio", "skullcandy", "jabra", "anker", "soundcore",
    "marshall", "harman", "beats", "airpods",

    # tvs
    "lg", "tcl", "hisense", "mi", "vu", "iffalcon",

    # shoes & fashion
    "nike", "adidas", "puma", "reebok", "new balance", "skechers",
    "converse", "vans", "under armour", "fila", "asics", "bata",
    "woodland", "red tape", "levi", "zara", "h&m",

    # appliances
    "whirlpool", "lg", "bosch", "samsung", "haier", "godrej",
    "voltas", "daikin", "carrier", "hitachi", "panasonic",
    "philips", "bajaj", "havells", "crompton", "usha",

    # cameras
    "canon", "nikon", "fujifilm", "gopro", "insta360",

    # gaming
    "playstation", "xbox", "nintendo", "logitech", "corsair",
    "razer", "steelseries", "hyperx",

    # tablets
    "ipad", "galaxy tab", "fire",

    # watches
    "fossil", "garmin", "fitbit", "amazfit", "noise", "titan",
    "casio", "seiko", "fastrack"
]

MODEL_CODE_PATTERN = re.compile(r'\b[A-Za-z]+\s?[A-Za-z]?\d+[A-Za-z0-9]*\b')


def _lines_from_boxes(boxes):
    grouped = defaultdict(list)
    for box in boxes:
        key = (box["block_num"], box["par_num"], box["line_num"])
        grouped[key].append(box)

    lines = []
    for _, words in grouped.items():
        words = sorted(words, key=lambda b: b["x"])
        text = " ".join(w["text"] for w in words).strip()
        avg_height = sum(w["h"] for w in words) / len(words)
        min_y = min(w["y"] for w in words)
        lines.append({"text": text, "height": avg_height, "y": min_y})

    return lines


def _clean_name(text):
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\d+\.\d+\s*[\(\d\)★\*]+', '', text)
    text = re.sub(r'\d+\s?(GB|TB|MP|mAh|W|inch|")', '', text, flags=re.IGNORECASE)
    parts = text.split('|')
    text = parts[0].strip()
    words = text.split()
    return " ".join(words[:5]).strip()


def _badge_score(text):
    tokens = [t.strip(".,\"'!*|").lower() for t in text.split()]
    tokens = [t for t in tokens if t]
    if not tokens:
        return 999
    bad = sum(1 for t in tokens if t in GENERIC_WORDS or t in SPEC_TOKENS)
    return bad / len(tokens)


def _has_brand(text):
    return any(brand in text.lower() for brand in KNOWN_BRANDS)


def get_product_title(boxes):
    lines = _lines_from_boxes(boxes)
    if not lines:
        return "Product not found"

    lines = sorted(lines, key=lambda l: l["y"])

    scored = []
    for l in lines:
        text = l["text"]
        letters = sum(c.isalpha() for c in text)
        if len(text) < 3 or letters < len(text) * 0.4:
            continue
        scored.append((l, _badge_score(text)))

    if not scored:
        return lines[0]["text"]

    brand_lines = [(l, s) for l, s in scored if _has_brand(l["text"]) and s < 0.6]
    if brand_lines:
        brand_lines.sort(key=lambda pair: (pair[1], pair[0]["y"]))
        return _clean_name(brand_lines[0][0]["text"])

    scored.sort(key=lambda pair: (pair[1], pair[0]["y"]))
    return _clean_name(scored[0][0]["text"])


def get_debug_lines(boxes):
    lines = _lines_from_boxes(boxes)
    lines = sorted(lines, key=lambda l: l["y"])
    debug = []
    for l in lines:
        text = l["text"]
        letters = sum(c.isalpha() for c in text)
        valid = len(text) >= 3 and letters >= len(text) * 0.4
        score = _badge_score(text) if valid else None
        debug.append({
            "text": text,
            "y": l["y"],
            "height": l["height"],
            "valid": valid,
            "score": score
        })
    return debug