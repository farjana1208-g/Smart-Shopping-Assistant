import streamlit as st
from PIL import Image
from ocr.detect_text import extract_text_with_boxes
from agent.title import get_product_title
from agent.search_reviews import search_product_reviews
from agent.search_alternatives import search_alternatives
from agent.smart_verdict import get_verdict
from agent.extract_alternatives import suggest_alternatives
from agent.chat import chat_about_product
from agent.category import detect_category, get_chat_buttons
from agent.compare import compare_products
from agent.history import load_history, save_to_history, clear_history

st.set_page_config(
    page_title="Smart Shopping Assistant",
    page_icon="🛍️",
    layout="wide"
)

st.markdown("""
    <style>
        .stApp { background-color: #f0f4ff; }

        .header-box {
            background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #3b82f6 100%);
            padding: 2.2rem 2.5rem;
            border-radius: 24px;
            margin-bottom: 1.8rem;
            box-shadow: 0 8px 32px rgba(37,99,235,0.25);
            position: relative;
            overflow: hidden;
        }
        .header-box::before {
            content: '';
            position: absolute;
            top: -40px;
            right: -40px;
            width: 180px;
            height: 180px;
            background: rgba(255,255,255,0.06);
            border-radius: 50%;
        }
        .header-box::after {
            content: '';
            position: absolute;
            bottom: -60px;
            right: 80px;
            width: 240px;
            height: 240px;
            background: rgba(255,255,255,0.04);
            border-radius: 50%;
        }
        .header-icon {
            font-size: 2.8rem;
            margin-bottom: 0.4rem;
            display: block;
        }
        .header-box h1 {
            color: white !important;
            font-size: 2.2rem !important;
            font-weight: 900 !important;
            margin: 0 0 0.4rem 0 !important;
            -webkit-text-fill-color: white !important;
            letter-spacing: -0.02em;
            line-height: 1.1;
        }
        .header-tagline {
            color: #bfdbfe;
            font-size: 1.05rem;
            font-weight: 400;
            margin: 0;
            line-height: 1.5;
        }
        .header-tagline strong {
            color: white;
            font-weight: 700;
        }
        .header-stats {
            display: flex;
            gap: 1.5rem;
            margin-top: 1.2rem;
            flex-wrap: wrap;
        }
        .header-stat {
            background: rgba(255,255,255,0.12);
            border-radius: 10px;
            padding: 0.4rem 0.9rem;
            color: white;
            font-size: 0.82rem;
            font-weight: 600;
            backdrop-filter: blur(4px);
        }

        [data-testid="stFileUploader"] {
            background: white;
            padding: 1rem;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(37,99,235,0.08);
            border: 2px dashed #93c5fd;
        }
        [data-testid="stImage"] {
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.10);
            margin-top: 0.8rem;
        }
        div.stButton > button {
            background: linear-gradient(90deg, #1e3a8a, #2563eb);
            color: white;
            border-radius: 12px;
            padding: 0.7rem 1.4rem;
            font-weight: 700;
            font-size: 1rem;
            border: none;
            width: 100%;
            box-shadow: 0 4px 14px rgba(37,99,235,0.3);
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg, #1e40af, #3b82f6);
            box-shadow: 0 6px 20px rgba(37,99,235,0.4);
            transform: translateY(-1px);
        }
        .product-card {
            background: white;
            padding: 1.2rem 1.5rem;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(37,99,235,0.08);
            border-left: 6px solid #2563eb;
            margin-bottom: 1rem;
        }
        .product-label {
            color: #2563eb;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .product-name {
            color: #111827;
            font-size: 1.5rem;
            font-weight: 800;
            margin-top: 0.2rem;
        }
        .badge-buy {
            display: inline-block;
            background: linear-gradient(90deg, #15803d, #16a34a);
            color: white;
            font-size: 1rem;
            font-weight: 800;
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            letter-spacing: 0.08em;
            margin-bottom: 0.8rem;
            box-shadow: 0 4px 12px rgba(22,163,74,0.3);
        }
        .badge-avoid {
            display: inline-block;
            background: linear-gradient(90deg, #b91c1c, #dc2626);
            color: white;
            font-size: 1rem;
            font-weight: 800;
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            letter-spacing: 0.08em;
            margin-bottom: 0.8rem;
            box-shadow: 0 4px 12px rgba(220,38,38,0.3);
        }
        .badge-wait {
            display: inline-block;
            background: linear-gradient(90deg, #b45309, #d97706);
            color: white;
            font-size: 1rem;
            font-weight: 800;
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            letter-spacing: 0.08em;
            margin-bottom: 0.8rem;
            box-shadow: 0 4px 12px rgba(217,119,6,0.3);
        }
        .badge-unknown {
            display: inline-block;
            background: #6b7280;
            color: white;
            font-size: 1rem;
            font-weight: 800;
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            letter-spacing: 0.08em;
            margin-bottom: 0.8rem;
        }
        .rating-box {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin-bottom: 0.8rem;
        }
        .rating-number {
            font-size: 2.5rem;
            font-weight: 900;
            color: #1e3a8a;
            line-height: 1;
        }
        .rating-label { color: #6b7280; font-size: 0.85rem; }
        .rating-bar-bg {
            background: #e5e7eb;
            border-radius: 50px;
            height: 10px;
            width: 100%;
            margin-top: 0.3rem;
        }
        .rating-bar-fill {
            background: linear-gradient(90deg, #2563eb, #16a34a);
            border-radius: 50px;
            height: 10px;
        }
        .verdict-card {
            background: white;
            padding: 1.3rem 1.5rem;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(37,99,235,0.08);
            margin-bottom: 1rem;
        }
        .summary-text {
            color: #1f2937;
            font-size: 0.95rem;
            line-height: 1.7;
            margin-bottom: 1rem;
        }
        .pros-cons-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        .pros-box {
            background: #f0fdf4;
            border: 1.5px solid #86efac;
            border-radius: 12px;
            padding: 0.9rem 1rem;
        }
        .cons-box {
            background: #fff7f7;
            border: 1.5px solid #fca5a5;
            border-radius: 12px;
            padding: 0.9rem 1rem;
        }
        .pros-title {
            color: #16a34a;
            font-weight: 700;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        .cons-title {
            color: #dc2626;
            font-weight: 700;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        .pros-item { color: #166534; font-size: 0.88rem; padding: 0.2rem 0; }
        .cons-item { color: #991b1b; font-size: 0.88rem; padding: 0.2rem 0; }
        .best-buy-box {
            background: #eff6ff;
            border: 1.5px solid #93c5fd;
            border-radius: 12px;
            padding: 0.8rem 1rem;
            color: #1e3a8a;
            font-size: 0.9rem;
            font-weight: 600;
        }
        .alt-card {
            background: white;
            padding: 0.9rem 1.2rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(37,99,235,0.07);
            margin-bottom: 0.6rem;
            border-left: 5px solid #f59e0b;
        }
        .alt-name { font-weight: 700; color: #92400e; font-size: 0.95rem; }
        .alt-reason { color: #4b5563; font-size: 0.88rem; margin-top: 0.2rem; }
        .review-card {
            background: white;
            padding: 1rem 1.2rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(37,99,235,0.07);
            margin-bottom: 0.7rem;
            border-left: 5px solid #7c3aed;
        }
        .review-title { font-weight: 700; font-size: 0.92rem; margin-bottom: 0.3rem; }
        .review-snippet { color: #4b5563; font-size: 0.88rem; line-height: 1.5; }
        .section-header {
            font-size: 1rem;
            font-weight: 700;
            color: #1e3a8a;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin: 1rem 0 0.6rem 0;
            padding-bottom: 0.3rem;
            border-bottom: 2px solid #bfdbfe;
        }
        .placeholder-box {
            text-align: center;
            color: #93c5fd;
            background: white;
            border-radius: 16px;
            padding: 2.5rem 1rem;
            box-shadow: 0 2px 10px rgba(37,99,235,0.06);
            font-size: 0.95rem;
            border: 2px dashed #bfdbfe;
        }
        .or-divider {
            text-align: center;
            color: #9ca3af;
            font-weight: 600;
            font-size: 0.9rem;
            margin: 0.8rem 0;
        }
        .chat-msg-user {
            background: linear-gradient(90deg, #1e3a8a, #2563eb);
            color: white;
            padding: 0.7rem 1rem;
            border-radius: 14px 14px 4px 14px;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            max-width: 85%;
            margin-left: auto;
            box-shadow: 0 2px 8px rgba(37,99,235,0.2);
        }
        .chat-msg-ai {
            background: white;
            color: #1f2937;
            padding: 0.7rem 1rem;
            border-radius: 14px 14px 14px 4px;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
            max-width: 85%;
            box-shadow: 0 2px 8px rgba(37,99,235,0.08);
            border-left: 3px solid #2563eb;
        }
        .chat-container {
            background: #f8faff;
            border-radius: 16px;
            padding: 1rem;
            border: 1.5px solid #bfdbfe;
            margin-bottom: 0.8rem;
            max-height: 300px;
            overflow-y: auto;
        }
        .winner-card {
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            color: white;
            padding: 1.5rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 1rem;
            box-shadow: 0 6px 24px rgba(37,99,235,0.3);
        }
        .winner-label {
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            opacity: 0.8;
            margin-bottom: 0.3rem;
        }
        .winner-name {
            font-size: 1.8rem;
            font-weight: 900;
            margin-bottom: 0.5rem;
        }
        .winner-reason {
            font-size: 0.9rem;
            opacity: 0.9;
            line-height: 1.6;
        }
        .compare-card {
            background: white;
            padding: 1.2rem;
            border-radius: 16px;
            box-shadow: 0 2px 12px rgba(37,99,235,0.08);
            margin-bottom: 1rem;
        }
        .history-card {
            background: white;
            padding: 1rem 1.2rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(37,99,235,0.07);
            margin-bottom: 0.7rem;
            border-left: 5px solid #2563eb;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .history-name {
            font-weight: 700;
            color: #111827;
            font-size: 1rem;
        }
        .history-meta {
            color: #6b7280;
            font-size: 0.82rem;
            margin-top: 0.2rem;
        }
        .history-badge {
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.3rem 0.8rem;
            border-radius: 50px;
        }
        h3 { display: none !important; }
        [data-testid="stTextInput"] input {
            border-radius: 10px;
            border: 2px solid #93c5fd;
            padding: 0.6rem 1rem;
            font-size: 1rem;
        }
        [data-testid="stTextInput"] input:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37,99,235,0.12);
        }
        [data-testid="stTabs"] [data-baseweb="tab"] {
            font-weight: 600;
            font-size: 0.95rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
    <div class="header-box">
        <span class="header-icon">🛍️</span>
        <h1>Smart Shopping Assistant</h1>
        <p class="header-tagline">
            Find out <strong>if it's worth buying</strong> before you spend —
            upload a screenshot or type any product name to get an instant
            AI-powered verdict, pros &amp; cons, reviews, and smarter alternatives.
        </p>
        <div class="header-stats">
            <div class="header-stat">✅ Instant Verdict</div>
            <div class="header-stat">📊 Pros &amp; Cons</div>
            <div class="header-stat">🔄 Alternatives</div>
            <div class="header-stat">💬 Ask Anything</div>
            <div class="header-stat">⚖️ Compare Products</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------- Tabs ----------
tab1, tab2, tab3 = st.tabs(["🔍 Analyze", "⚖️ Compare", "📋 History"])

# ================================================================
# TAB 1 — ANALYZE
# ================================================================
with tab1:
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="section-header">📷 Upload Image or Enter Name</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drop a product screenshot here",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
            key="analyze_uploader"
        )
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
        st.markdown('<div class="or-divider">── OR ──</div>', unsafe_allow_html=True)
        manual_name = st.text_input(
            "Type product name",
            placeholder="e.g. Samsung Galaxy A55, Nike Air Max, Sony WH-1000XM5...",
            label_visibility="collapsed",
            key="analyze_input"
        )

    with col2:
        st.markdown('<div class="section-header">✨ Results</div>', unsafe_allow_html=True)
        has_input = uploaded_file is not None or (manual_name and manual_name.strip() != "")

        if has_input:
            if st.button("🔍 Analyze Product", key="analyze_btn"):

                if manual_name and manual_name.strip():
                    product_name = manual_name.strip()
                else:
                    with st.spinner("🔎 Detecting product from image..."):
                        boxes = extract_text_with_boxes(image)
                        product_name = get_product_title(boxes)

                category = detect_category(product_name)

                st.markdown(f"""
                    <div class="product-card">
                        <div class="product-label">Detected Product</div>
                        <div class="product-name">{product_name}</div>
                    </div>
                """, unsafe_allow_html=True)

                with st.spinner("📝 Searching reviews..."):
                    reviews = search_product_reviews(product_name)

                with st.spinner("🤖 Generating verdict..."):
                    verdict = get_verdict(product_name, reviews)

                badge = verdict.get("badge", "UNKNOWN").upper()
                badge_emoji = {"BUY": "✅", "AVOID": "❌", "WAIT FOR SALE": "⏳"}.get(badge, "❓")
                badge_class = {"BUY": "badge-buy", "AVOID": "badge-avoid", "WAIT FOR SALE": "badge-wait"}.get(badge, "badge-unknown")
                rating = verdict.get("rating", 0)
                rating_pct = int((float(rating) / 10) * 100)
                pros = verdict.get("pros", [])
                cons = verdict.get("cons", [])
                summary = verdict.get("summary", "")
                best_buy = verdict.get("best_place_to_buy", "")

                pros_html = "".join(f'<div class="pros-item">✅ {p}</div>' for p in pros)
                cons_html = "".join(f'<div class="cons-item">❌ {c}</div>' for c in cons)

                st.markdown(f"""
                    <div class="verdict-card">
                        <span class="{badge_class}">{badge_emoji} {badge}</span>
                        <div class="rating-box">
                            <div>
                                <div class="rating-number">{rating}</div>
                                <div class="rating-label">out of 10</div>
                            </div>
                            <div style="flex:1">
                                <div style="color:#6b7280; font-size:0.8rem; margin-bottom:0.3rem;">Overall Score</div>
                                <div class="rating-bar-bg">
                                    <div class="rating-bar-fill" style="width:{rating_pct}%"></div>
                                </div>
                            </div>
                        </div>
                        <div class="summary-text">{summary}</div>
                        <div class="pros-cons-grid">
                            <div class="pros-box">
                                <div class="pros-title">👍 Pros</div>
                                {pros_html}
                            </div>
                            <div class="cons-box">
                                <div class="cons-title">👎 Cons</div>
                                {cons_html}
                            </div>
                        </div>
                        <div class="best-buy-box">🛒 {best_buy}</div>
                    </div>
                """, unsafe_allow_html=True)

                with st.spinner("🔄 Finding alternatives..."):
                    alt_results = search_alternatives(product_name)
                    alternatives = suggest_alternatives(product_name, alt_results)

                if alternatives:
                    st.markdown('<div class="section-header">🔄 You Might Also Consider</div>', unsafe_allow_html=True)
                    for a in alternatives:
                        if isinstance(a, dict):
                            st.markdown(f"""
                                <div class="alt-card">
                                    <div class="alt-name">{a.get('name','')}</div>
                                    <div class="alt-reason">{a.get('reason','')}</div>
                                </div>
                            """, unsafe_allow_html=True)

                if reviews:
                    st.markdown('<div class="section-header">📝 What People Are Saying</div>', unsafe_allow_html=True)
                    for r in reviews:
                        if isinstance(r, dict):
                            st.markdown(f"""
                                <div class="review-card">
                                    <div class="review-title">
                                        <a href="{r.get('url','#')}" target="_blank" style="color:#7c3aed; text-decoration:none;">
                                            {r.get('title','')}
                                        </a>
                                    </div>
                                    <div class="review-snippet">{r.get('snippet','')}</div>
                                </div>
                            """, unsafe_allow_html=True)

                st.session_state["product_name"] = product_name
                st.session_state["verdict"] = verdict
                st.session_state["reviews"] = reviews
                st.session_state["category"] = category
                st.session_state["chat_history"] = []
                st.session_state["analyzed"] = True
                save_to_history(product_name, verdict, category)

        else:
            st.markdown("""
                <div class='placeholder-box'>
                    <div style='font-size:2rem; margin-bottom:0.5rem'>👈</div>
                    <div style='font-weight:700; color:#1e3a8a; margin-bottom:0.3rem'>Ready to help you shop smarter</div>
                    <div>Upload a product screenshot or type a name on the left to get started</div>
                </div>
            """, unsafe_allow_html=True)

    # ---------- Chat ----------
    if st.session_state.get("analyzed"):
        st.divider()
        st.markdown('<div class="section-header">💬 Ask About This Product</div>', unsafe_allow_html=True)

        product_name = st.session_state.get("product_name", "this product")
        category = st.session_state.get("category", "general")
        chat_buttons = get_chat_buttons(category)

        if st.session_state.get("chat_history"):
            chat_html = ""
            for msg in st.session_state["chat_history"]:
                if msg["role"] == "user":
                    chat_html += f'<div class="chat-msg-user">{msg["content"]}</div>'
                else:
                    chat_html += f'<div class="chat-msg-ai">{msg["content"]}</div>'
            st.markdown(f'<div class="chat-container">{chat_html}</div>', unsafe_allow_html=True)

        st.markdown("**Quick questions:**")
        cols1 = st.columns(3)
        for i, (label, question) in enumerate(chat_buttons[:3]):
            with cols1[i]:
                if st.button(label, key=f"q1_{i}"):
                    st.session_state["pending_question"] = question

        cols2 = st.columns(3)
        for i, (label, question) in enumerate(chat_buttons[3:6]):
            with cols2[i]:
                if st.button(label, key=f"q2_{i}"):
                    st.session_state["pending_question"] = question

        user_input = st.text_input(
            "Or ask anything...",
            placeholder="e.g. I'm a student with ₹20,000 budget — should I buy this?",
            key="chat_input"
        )

        question = st.session_state.pop("pending_question", None) or (user_input.strip() if user_input else None)

        if question:
            with st.spinner("🤖 Searching and thinking..."):
                response = chat_about_product(
                    product_name=st.session_state["product_name"],
                    verdict=st.session_state["verdict"],
                    reviews=st.session_state["reviews"],
                    chat_history=st.session_state["chat_history"],
                    user_message=question
                )
            st.session_state["chat_history"].append({"role": "user", "content": question})
            st.session_state["chat_history"].append({"role": "assistant", "content": response})
            st.rerun()

# ================================================================
# TAB 2 — COMPARE
# ================================================================
with tab2:
    st.markdown('<div class="section-header">⚖️ Compare Two Products</div>', unsafe_allow_html=True)
    st.markdown("Not sure which one to pick? Type two product names below and get a side-by-side breakdown with a clear winner.")

    comp_col1, comp_col2 = st.columns(2, gap="large")
    with comp_col1:
        st.markdown("**Product 1**")
        p1_name = st.text_input("Product 1", placeholder="e.g. vivo T5x", label_visibility="collapsed", key="compare_p1")
    with comp_col2:
        st.markdown("**Product 2**")
        p2_name = st.text_input("Product 2", placeholder="e.g. Realme P4R", label_visibility="collapsed", key="compare_p2")

    if st.button("⚖️ Compare Products", key="compare_btn"):
        if p1_name.strip() and p2_name.strip():
            col_a, col_b = st.columns(2, gap="large")

            with col_a:
                with st.spinner(f"Analyzing {p1_name}..."):
                    reviews1 = search_product_reviews(p1_name)
                    verdict1 = get_verdict(p1_name, reviews1)
                badge1 = verdict1.get("badge", "UNKNOWN").upper()
                badge_emoji1 = {"BUY": "✅", "AVOID": "❌", "WAIT FOR SALE": "⏳"}.get(badge1, "❓")
                badge_class1 = {"BUY": "badge-buy", "AVOID": "badge-avoid", "WAIT FOR SALE": "badge-wait"}.get(badge1, "badge-unknown")
                rating1 = verdict1.get("rating", 0)
                rating_pct1 = int((float(rating1) / 10) * 100)
                pros1 = "".join(f'<div class="pros-item">✅ {p}</div>' for p in verdict1.get("pros", []))
                cons1 = "".join(f'<div class="cons-item">❌ {c}</div>' for c in verdict1.get("cons", []))
                st.markdown(f"""
                    <div class="compare-card">
                        <div class="product-name" style="font-size:1.2rem">{p1_name}</div>
                        <br>
                        <span class="{badge_class1}">{badge_emoji1} {badge1}</span>
                        <div class="rating-box" style="margin-top:0.8rem">
                            <div>
                                <div class="rating-number">{rating1}</div>
                                <div class="rating-label">out of 10</div>
                            </div>
                            <div style="flex:1">
                                <div class="rating-bar-bg">
                                    <div class="rating-bar-fill" style="width:{rating_pct1}%"></div>
                                </div>
                            </div>
                        </div>
                        <div class="pros-cons-grid">
                            <div class="pros-box"><div class="pros-title">👍 Pros</div>{pros1}</div>
                            <div class="cons-box"><div class="cons-title">👎 Cons</div>{cons1}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with col_b:
                with st.spinner(f"Analyzing {p2_name}..."):
                    reviews2 = search_product_reviews(p2_name)
                    verdict2 = get_verdict(p2_name, reviews2)
                badge2 = verdict2.get("badge", "UNKNOWN").upper()
                badge_emoji2 = {"BUY": "✅", "AVOID": "❌", "WAIT FOR SALE": "⏳"}.get(badge2, "❓")
                badge_class2 = {"BUY": "badge-buy", "AVOID": "badge-avoid", "WAIT FOR SALE": "badge-wait"}.get(badge2, "badge-unknown")
                rating2 = verdict2.get("rating", 0)
                rating_pct2 = int((float(rating2) / 10) * 100)
                pros2 = "".join(f'<div class="pros-item">✅ {p}</div>' for p in verdict2.get("pros", []))
                cons2 = "".join(f'<div class="cons-item">❌ {c}</div>' for c in verdict2.get("cons", []))
                st.markdown(f"""
                    <div class="compare-card">
                        <div class="product-name" style="font-size:1.2rem">{p2_name}</div>
                        <br>
                        <span class="{badge_class2}">{badge_emoji2} {badge2}</span>
                        <div class="rating-box" style="margin-top:0.8rem">
                            <div>
                                <div class="rating-number">{rating2}</div>
                                <div class="rating-label">out of 10</div>
                            </div>
                            <div style="flex:1">
                                <div class="rating-bar-bg">
                                    <div class="rating-bar-fill" style="width:{rating_pct2}%"></div>
                                </div>
                            </div>
                        </div>
                        <div class="pros-cons-grid">
                            <div class="pros-box"><div class="pros-title">👍 Pros</div>{pros2}</div>
                            <div class="cons-box"><div class="cons-title">👎 Cons</div>{cons2}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            with st.spinner("🏆 Determining winner..."):
                comparison = compare_products(p1_name, verdict1, p2_name, verdict2)

            winner = comparison.get("winner", "Unknown")
            reason = comparison.get("reason", "")
            best_budget = comparison.get("best_for_budget", "")
            best_quality = comparison.get("best_for_quality", "")

            st.markdown(f"""
                <div class="winner-card">
                    <div class="winner-label">🏆 Winner</div>
                    <div class="winner-name">{winner}</div>
                    <div class="winner-reason">{reason}</div>
                </div>
                <div class="compare-card">
                    <div style="margin-bottom:0.5rem"><b>💰 Best for budget:</b> {best_budget}</div>
                    <div><b>⭐ Best for quality:</b> {best_quality}</div>
                </div>
            """, unsafe_allow_html=True)

            save_to_history(p1_name, verdict1, detect_category(p1_name))
            save_to_history(p2_name, verdict2, detect_category(p2_name))
        else:
            st.warning("Please enter both product names to compare.")

# ================================================================
# TAB 3 — HISTORY
# ================================================================
with tab3:
    st.markdown('<div class="section-header">📋 Analysis History</div>', unsafe_allow_html=True)
    st.markdown("Every product you analyze gets saved here so you can revisit your research anytime.")

    history = load_history()

    if history:
        if st.button("🗑️ Clear All History", key="clear_history"):
            clear_history()
            st.success("History cleared.")
            st.rerun()

        for entry in history:
            badge = entry.get("badge", "UNKNOWN")
            badge_color = {"BUY": "#16a34a", "AVOID": "#dc2626", "WAIT FOR SALE": "#d97706"}.get(badge, "#6b7280")
            badge_emoji = {"BUY": "✅", "AVOID": "❌", "WAIT FOR SALE": "⏳"}.get(badge, "❓")
            rating = entry.get("rating", 0)
            timestamp = entry.get("timestamp", "")
            category = entry.get("category", "general")

            st.markdown(f"""
                <div class="history-card">
                    <div>
                        <div class="history-name">{entry.get('product_name','')}</div>
                        <div class="history-meta">⭐ {rating}/10 &nbsp;|&nbsp; 📦 {category.capitalize()} &nbsp;|&nbsp; 🕐 {timestamp}</div>
                    </div>
                    <span class="history-badge" style="background:{badge_color}; color:white;">
                        {badge_emoji} {badge}
                    </span>
                </div>
            """, unsafe_allow_html=True)

            with st.expander(f"View details — {entry.get('product_name','')}"):
                st.markdown(f"**Summary:** {entry.get('summary','')}")
                pros = entry.get("pros", [])
                cons = entry.get("cons", [])
                if pros:
                    st.markdown("**👍 Pros:** " + " | ".join(pros))
                if cons:
                    st.markdown("**👎 Cons:** " + " | ".join(cons))
    else:
        st.markdown("""
            <div class='placeholder-box'>
                <div style='font-size:2rem; margin-bottom:0.5rem'>📋</div>
                <div style='font-weight:700; color:#1e3a8a; margin-bottom:0.3rem'>No history yet</div>
                <div>Analyze a product and it will appear here automatically</div>
            </div>
        """, unsafe_allow_html=True)