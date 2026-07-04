def detect_category(product_name):
    """
    Detect product category from product name.
    Returns category string.
    """
    lower = product_name.lower()

    phone_brands = ["vivo", "samsung", "redmi", "xiaomi", "realme", "oppo",
                    "oneplus", "iphone", "nokia", "asus", "poco", "infinix",
                    "tecno", "motorola", "moto", "pixel", "honor", "nothing", "iqoo"]

    laptop_keywords = ["laptop", "notebook", "macbook", "chromebook", "thinkpad",
                       "ideapad", "inspiron", "pavilion", "zenbook", "vivobook",
                       "predator", "dell", "hp", "acer", "msi", "razer", "surface"]

    audio_keywords = ["earphone", "headphone", "earbuds", "speaker", "audio",
                      "bose", "sony wh", "jbl", "sennheiser", "boat", "boult",
                      "noise", "beats", "airpods", "soundbar"]

    tv_keywords = ["tv", "television", "smart tv", "oled tv", "qled", "lg oled",
                   "samsung tv", "tcl", "hisense", "vu tv"]

    shoe_keywords = ["nike", "adidas", "puma", "shoe", "sneaker", "boot",
                     "sandal", "slipper", "reebok", "converse", "vans",
                     "new balance", "skechers", "jordan"]

    appliance_keywords = ["washing machine", "refrigerator", "fridge", "ac ",
                          "air conditioner", "microwave", "mixer", "grinder",
                          "vacuum", "iron", "fan", "cooler", "water purifier"]

    camera_keywords = ["camera", "canon", "nikon", "fujifilm", "gopro",
                       "dslr", "mirrorless", "lens"]

    watch_keywords = ["watch", "smartwatch", "fossil", "garmin", "fitbit",
                      "amazfit", "casio", "titan", "fastrack"]

    gaming_keywords = ["playstation", "xbox", "nintendo", "controller",
                       "gaming mouse", "gaming keyboard", "headset", "gpu",
                       "graphics card"]

    tablet_keywords = ["ipad", "tablet", "galaxy tab", "fire tablet"]

    if any(b in lower for b in phone_brands) or "phone" in lower or "5g" in lower:
        return "phone"
    elif any(k in lower for k in laptop_keywords):
        return "laptop"
    elif any(k in lower for k in audio_keywords):
        return "audio"
    elif any(k in lower for k in tv_keywords):
        return "tv"
    elif any(k in lower for k in shoe_keywords):
        return "shoe"
    elif any(k in lower for k in appliance_keywords):
        return "appliance"
    elif any(k in lower for k in camera_keywords):
        return "camera"
    elif any(k in lower for k in watch_keywords):
        return "watch"
    elif any(k in lower for k in gaming_keywords):
        return "gaming"
    elif any(k in lower for k in tablet_keywords):
        return "tablet"
    else:
        return "general"


def get_chat_buttons(category):
    """
    Returns smart chat button labels based on product category.
    """
    buttons = {
        "phone": [
            ("🎮 Good for gaming?", "Is it good for gaming?"),
            ("📸 Camera quality?", "How is the camera quality?"),
            ("🔋 Battery life?", "How is the battery life?"),
            ("🎓 Good for students?", "I am a student. Should I buy this?"),
            ("💼 Good for work?", "Is it good for work and productivity?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ],
        "laptop": [
            ("💻 Good for coding?", "Is it good for coding and programming?"),
            ("🎮 Good for gaming?", "Is it good for gaming?"),
            ("🔋 Battery life?", "How is the battery life for daily use?"),
            ("🎓 Good for students?", "I am a student. Should I buy this laptop?"),
            ("🎨 Good for design?", "Is it good for graphic design and video editing?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ],
        "audio": [
            ("🎵 Sound quality?", "How is the sound quality?"),
            ("🔇 Noise cancellation?", "How is the noise cancellation?"),
            ("🔋 Battery life?", "How is the battery life?"),
            ("🏃 Good for workouts?", "Is it good for working out and sports?"),
            ("📞 Good for calls?", "Is it good for phone calls?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ],
        "tv": [
            ("🖼️ Picture quality?", "How is the picture quality?"),
            ("🔊 Sound quality?", "How is the built-in sound quality?"),
            ("📺 Good for movies?", "Is it good for watching movies?"),
            ("🎮 Good for gaming?", "Is it good for gaming on consoles?"),
            ("📡 Smart features?", "How are the smart TV features and apps?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ],
        "shoe": [
            ("👟 True to size?", "Is it true to size?"),
            ("🏃 Good for running?", "Is it good for running?"),
            ("😌 Comfortable?", "How comfortable is it for daily wear?"),
            ("💪 Durable?", "How durable is it?"),
            ("👗 Stylish?", "Is it stylish and good looking?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ],
        "appliance": [
            ("⚡ Energy efficient?", "How energy efficient is it?"),
            ("🔧 Easy to use?", "Is it easy to use and maintain?"),
            ("📦 Easy to install?", "Is it easy to install?"),
            ("🔊 Noise level?", "How noisy is it during operation?"),
            ("🛠️ After sales service?", "How is the after sales service?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ],
        "camera": [
            ("📸 Image quality?", "How is the image quality?"),
            ("🎥 Video quality?", "How is the video quality?"),
            ("🌙 Low light performance?", "How does it perform in low light?"),
            ("🏃 Good for action shots?", "Is it good for action and sports photography?"),
            ("🔋 Battery life?", "How is the battery life?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ],
        "watch": [
            ("❤️ Health tracking?", "How accurate is the health and fitness tracking?"),
            ("🔋 Battery life?", "How is the battery life?"),
            ("💧 Waterproof?", "Is it waterproof and suitable for swimming?"),
            ("📱 Phone compatibility?", "Is it compatible with Android and iPhone?"),
            ("😌 Comfortable?", "Is it comfortable to wear all day?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ],
        "gaming": [
            ("🎮 Performance?", "How is the gaming performance?"),
            ("🖥️ Compatible with?", "What devices is it compatible with?"),
            ("😌 Comfortable?", "Is it comfortable for long gaming sessions?"),
            ("🔊 Audio quality?", "How is the audio quality?"),
            ("🔧 Build quality?", "How is the build quality and durability?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ],
        "tablet": [
            ("💻 Good for work?", "Is it good for work and productivity?"),
            ("🎨 Good for drawing?", "Is it good for digital art and drawing?"),
            ("🎮 Good for gaming?", "Is it good for gaming?"),
            ("🔋 Battery life?", "How is the battery life?"),
            ("🎓 Good for students?", "Is it good for students?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ],
        "general": [
            ("✅ Main strengths?", "What are the main strengths of this product?"),
            ("❌ Main weaknesses?", "What are the main weaknesses?"),
            ("🎓 Good for beginners?", "Is it good for beginners?"),
            ("💪 How durable?", "How durable and long lasting is it?"),
            ("🛠️ After sales service?", "How is the after sales service?"),
            ("💰 Worth the price?", "Is it worth the price?"),
        ]
    }
    return buttons.get(category, buttons["general"])