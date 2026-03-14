import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import streamlit.components.v1 as components

from app.blog_generator import generate_blog
from app.tweet_generator import generate_tweet
from app.caption_generator import generate_caption
from app.linkedin_generator import generate_linkedin_post

st.set_page_config(
    page_title="AI Content Engine",
    page_icon="assets/icon.png",
    layout="centered"
)

# ── Load background image as base64 so Streamlit can serve it ─────────────────
import base64

def _get_base64_bg(path: str) -> str:
    """Read an image file and return a CSS-ready base64 data-URI."""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = path.rsplit(".", 1)[-1].lower()
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    return f"data:{mime};base64,{data}"

# bg.jpg lives in the same folder as this script (ui/)
_bg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bg.jpg")
_bg_uri  = _get_base64_bg(_bg_path)

# Inject as a CSS variable so the existing stylesheet can reference it
st.markdown(
    f"<style>:root {{ --bg-image: url('{_bg_uri}'); }}</style>",
    unsafe_allow_html=True,
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>

/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&display=swap');

/* ── Root tokens ── */
:root {
    --bg:           #050a14;
    --surface:      rgba(6, 14, 30, 0.60);
    --surface-2:    rgba(8, 20, 50, 0.40);
    --surface-solid: #0a1428;
    --border:       rgba(100,200,255,0.10);
    --border-focus: rgba(0,210,255,0.50);
    --accent:       #00d2ff;
    --accent-2:     #38f0b8;
    --accent-warm:  #f6ad55;
    --text-primary: #e4eef8;
    --text-muted:   #90b8d8;
    --text-faint:   #5a7898;
    --radius-sm:    9px;
    --radius-md:    14px;
    --radius-lg:    20px;
    --shadow-card:  0 8px 40px rgba(0,0,0,0.7);
    --font-head:    'Outfit', sans-serif;
    --font-body:    'Plus Jakarta Sans', sans-serif;
    --glass-blur:   blur(18px);
}

/* ── Background image ── */
html, body {
    background: var(--bg) !important;
}
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(180deg, rgba(5,10,20,0.45) 0%, rgba(5,10,20,0.70) 100%),
        var(--bg-image) center center / cover no-repeat fixed !important;
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}

/* Subtle cyan vignette over bg to complement the network glow */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 55% 45% at 80% 60%, rgba(0,180,255,0.07) 0%, transparent 65%),
        radial-gradient(ellipse 35% 30% at 10% 90%, rgba(0,210,255,0.05) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

[data-testid="stMain"] { position: relative; z-index: 1; }

/* ── Hide sidebar collapse/expand button (shows raw icon text when font fails) ── */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[kind="header"] {
    display: none !important;
}

/* ── Sidebar — frosted glass panel ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    backdrop-filter: var(--glass-blur) !important;
    -webkit-backdrop-filter: var(--glass-blur) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 1.5rem 1.25rem; }
[data-testid="stSidebar"] * { font-family: var(--font-body) !important; }

/* Sidebar heading */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: var(--font-head) !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    margin-bottom: 1.1rem !important;
}

/* Sidebar expanders — frosted glass */
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: rgba(0,180,255,0.05) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(0,210,255,0.12) !important;
    border-radius: var(--radius-sm) !important;
    margin-bottom: 0.5rem !important;
    overflow: hidden !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    padding: 0.65rem 0.9rem !important;
    list-style: none !important;
}
/* Hide broken Material Icons arrow that renders as raw "_arrow_right" text */
[data-testid="stSidebar"] [data-testid="stExpander"] summary svg,
[data-testid="stSidebar"] [data-testid="stExpander"] summary [data-testid="stExpanderToggleIcon"],
[data-testid="stSidebar"] details summary > div > span[class*="material"],
[data-testid="stSidebar"] details summary > div > svg {
    display: none !important;
}
/* Prevent icon font fallback text bleeding through */
[data-testid="stSidebar"] [data-testid="stExpander"] summary * {
    font-family: var(--font-body) !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
    color: var(--accent) !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] > div > div {
    font-size: 0.8rem !important;
    color: var(--text-muted) !important;
    padding: 0 0.9rem 0.75rem !important;
    line-height: 1.6 !important;
}

/* ── Main content wrapper ── */
[data-testid="stMain"] .block-container {
    max-width: 760px !important;
    padding: 3rem 2rem 4rem !important;
}

/* ── Typography ── */
h1 {
    font-family: var(--font-head) !important;
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.01em !important;
    line-height: 1.15 !important;
    color: var(--text-primary) !important;
    margin-bottom: 0 !important;
}
h2, h3 {
    font-family: var(--font-head) !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
}
p, li { font-family: var(--font-body) !important; }

/* ── Labels ── */
label, [data-testid="stWidgetLabel"] p {
    font-family: var(--font-body) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    margin-bottom: 6px !important;
}

/* ── Inputs & textareas — frosted glass ── */
input[type="text"],
textarea,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background: rgba(8, 20, 50, 0.40) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(0,210,255,0.20) !important;
    border-radius: var(--radius-sm) !important;
    color: #cce0f5 !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s, background 0.2s !important;
    caret-color: var(--accent) !important;
}
input[type="text"]:focus,
textarea:focus,
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px rgba(0,210,255,0.10), 0 0 18px rgba(0,210,255,0.08) !important;
    outline: none !important;
}

/* ── Selects / dropdowns — frosted glass ── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(8, 20, 50, 0.40) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(0,210,255,0.20) !important;
    border-radius: var(--radius-sm) !important;
    color: #cce0f5 !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--border-focus) !important;
}
/* dropdown option list */
[data-testid="stSelectboxVirtualDropdown"],
[data-baseweb="popover"] ul {
    background: #071020 !important;
    border: 1px solid rgba(0,210,255,0.15) !important;
    border-radius: var(--radius-sm) !important;
}
[data-baseweb="popover"] li {
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.92rem !important;
}
[data-baseweb="popover"] li:hover {
    background: rgba(0,210,255,0.08) !important;
}

/* ── Primary Generate button — cyan glow ── */
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #00d2ff 0%, #0080cc 100%) !important;
    color: #020d1a !important;
    font-family: var(--font-head) !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.7rem 1.8rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s !important;
    box-shadow: 0 4px 22px rgba(0,210,255,0.30), 0 0 0 1px rgba(0,210,255,0.15) !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(0,210,255,0.42), 0 0 0 1px rgba(0,210,255,0.25) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: rgba(8, 20, 50, 0.40) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(0,210,255,0.20) !important;
    color: #90b8d8 !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.55rem 1.2rem !important;
    transition: border-color 0.2s, color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border-color: rgba(0,210,255,0.45) !important;
    color: var(--accent) !important;
    box-shadow: 0 0 12px rgba(0,210,255,0.12) !important;
}

/* ── Sidebar clear history button ── */
[data-testid="stSidebar"] [data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid rgba(0,210,255,0.10) !important;
    color: var(--text-faint) !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    padding: 0.45rem 1rem !important;
    box-shadow: none !important;
    margin-top: 0.75rem !important;
    width: 100% !important;
    transition: border-color 0.2s, color 0.2s, background 0.2s !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    border-color: rgba(255,80,80,0.4) !important;
    color: #fc8181 !important;
    background: rgba(255,80,80,0.06) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── Warning banner ── */
[data-testid="stAlert"] {
    background: rgba(246,173,85,0.07) !important;
    border: 1px solid rgba(246,173,85,0.22) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--accent-warm) !important;
    backdrop-filter: blur(6px) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    color: var(--text-muted) !important;
    font-size: 0.88rem !important;
    font-family: var(--font-body) !important;
}

/* ── Dividers ── */
hr {
    border-color: var(--border) !important;
    margin: 2rem 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,180,255,0.15); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,180,255,0.28); }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:1.4rem;">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
             fill="none" stroke="#00d2ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
             style="opacity:0.6;">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12 6 12 12 16 14"/>
        </svg>
        <span style="font-family:'Outfit',sans-serif;font-size:0.78rem;font-weight:600;
                     letter-spacing:0.12em;text-transform:uppercase;color:#6a90b8;">
          Content History
        </span>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        for item in reversed(st.session_state.history):
            label = f"{item['type']}  ·  {item['topic']}"
            preview = item["content"][:120].replace("<","&lt;").replace(">","&gt;")
            if len(item["content"]) > 120:
                preview += "…"
            st.markdown(f"""
            <div style="background:rgba(0,180,255,0.05);border:1px solid rgba(0,210,255,0.12);
                        border-radius:8px;padding:0.65rem 0.9rem;margin-bottom:0.5rem;
                        cursor:default;">
                <div style="font-family:'Outfit',sans-serif;font-size:0.76rem;font-weight:600;
                            letter-spacing:0.04em;color:#90b8d8;margin-bottom:5px;">
                    {label}
                </div>
                <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:0.78rem;
                            color:#5a7898;line-height:1.55;">
                    {preview}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p style="font-size:0.82rem;color:#6a90b8;margin-top:0.25rem;line-height:1.6;">
            Nothing here yet.<br>Generate your first piece of content to see it here.
        </p>
        """, unsafe_allow_html=True)

    if st.button("Clear History", key="clear_history"):
        st.session_state.history = []
        st.rerun()

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:0.5rem;">
    <div style="display:inline-flex;align-items:center;gap:9px;
                background:rgba(0,210,255,0.07);border:1px solid rgba(0,210,255,0.20);
                border-radius:100px;padding:5px 14px;margin-bottom:1.2rem;">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"
             fill="none" stroke="#00d2ff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
        </svg>
        <span style="font-family:'Outfit',sans-serif;font-size:0.7rem;font-weight:600;
                     letter-spacing:0.12em;text-transform:uppercase;color:#00d2ff;">
          Powered by Gemini AI
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

st.title("AI Content Engine")

st.markdown("""
<p style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.05rem;font-weight:300;
           color:#6a90b8;line-height:1.75;margin-top:0.5rem;margin-bottom:2.2rem;
           max-width:560px;">
  Generate polished blog posts, tweets, Instagram captions, and LinkedIn posts
  in seconds — tailored to your topic and tone.
</p>
""", unsafe_allow_html=True)

# ── Thin divider ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="width:100%;height:1px;background:linear-gradient(
    90deg,transparent,rgba(255,255,255,0.07) 30%,rgba(255,255,255,0.07) 70%,transparent);
    margin-bottom:2rem;"></div>
""", unsafe_allow_html=True)

# ── Form section label ────────────────────────────────────────────────────────
st.markdown("""
<p style="font-family:'Outfit',sans-serif;font-size:0.7rem;font-weight:600;
           letter-spacing:0.14em;text-transform:uppercase;color:#5a7898;
           margin-bottom:1.4rem;">
  Configure your content
</p>
""", unsafe_allow_html=True)

# ── Content type ──────────────────────────────────────────────────────────────
content_type = st.selectbox(
    "Content Type",
    ["Blog Post", "Tweet", "Instagram Caption", "LinkedIn Post"]
)

# ── Topic ─────────────────────────────────────────────────────────────────────
topic = st.text_input(
    "Topic",
    placeholder="e.g. The future of remote work in 2025"
)

# ── LinkedIn style (conditional) ─────────────────────────────────────────────
user_style = None
if content_type == "LinkedIn Post":
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-top:0.25rem;">
        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"
             fill="none" stroke="#4a5068" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <span style="font-size:0.76rem;color:#4a5068;">
          Paste a sample post to let the AI mirror your writing style.
        </span>
    </div>
    """, unsafe_allow_html=True)
    user_style = st.text_area(
        "LinkedIn Style Sample  (optional)",
        placeholder="Example:\n I'm excited to share...\n\nKey insights:\n1. ...\n2. ...\n\n#AI #Tech",
        height=120
    )

# ── Tone ──────────────────────────────────────────────────────────────────────
tone = st.selectbox(
    "Tone",
    ["Professional", "Casual", "Funny", "Motivational", "Inspirational"]
)

st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

# ── Generate button ───────────────────────────────────────────────────────────
generate = st.button("Generate Content", use_container_width=True)

# ── Generation logic ──────────────────────────────────────────────────────────
if generate:
    if not topic:
        st.warning("Please enter a topic before generating.")
    else:
        with st.spinner("Composing your content…"):
            if content_type == "Blog Post":
                result = generate_blog(topic, tone)
            elif content_type == "Tweet":
                result = generate_tweet(topic, tone)
            elif content_type == "LinkedIn Post":
                result = generate_linkedin_post(topic, tone, user_style)
            else:
                result = generate_caption(topic, tone)

        st.session_state.history.append({
            "type": content_type,
            "topic": topic,
            "content": result
        })

        # ── Output card header ─────────────────────────────────────────────
        st.markdown("""
        <div style="width:100%;height:1px;
                    background:linear-gradient(90deg,transparent,rgba(0,210,255,0.12) 30%,
                    rgba(0,210,255,0.12) 70%,transparent);margin:2.2rem 0 1.8rem;"></div>

        <div style="display:flex;align-items:center;justify-content:space-between;
                    margin-bottom:1rem;">
            <div style="display:flex;align-items:center;gap:10px;">
                <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"
                     fill="none" stroke="#38f0b8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"/>
                </svg>
                <span style="font-family:'Outfit',sans-serif;font-size:0.7rem;font-weight:600;
                             letter-spacing:0.14em;text-transform:uppercase;color:#38f0b8;">
                  Generated Content
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Output card body ───────────────────────────────────────────────
        safe_result = result.replace("`", "&#96;").replace("</", "<\\/")
        st.markdown(f"""
        <div style="background:rgba(5,14,32,0.82);
                    backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
                    border:1px solid rgba(0,210,255,0.12);
                    border-radius:14px;padding:1.6rem 1.8rem;
                    box-shadow:0 8px 40px rgba(0,0,0,0.65), 0 0 0 1px rgba(0,210,255,0.06);
                    font-family:'Plus Jakarta Sans',sans-serif;font-size:0.95rem;
                    line-height:1.85;color:#c0d4e8;
                    white-space:pre-wrap;word-break:break-word;">
            {safe_result}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── Action buttons row ────────────────────────────────────────────
        col1, col2 = st.columns([1, 1])

        with col1:
            # Copy button via HTML component
            components.html(
                f"""
                <style>
                  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500&display=swap');
                  * {{ margin:0;padding:0;box-sizing:border-box; }}
                  button {{
                    width: 100%;
                    background: rgba(5,14,32,0.80);
                    border: 1px solid rgba(0,210,255,0.15);
                    color: #6a90b8;
                    font-family: 'Plus Jakarta Sans', sans-serif;
                    font-size: 0.84rem;
                    font-weight: 500;
                    border-radius: 9px;
                    padding: 9px 18px;
                    cursor: pointer;
                    display: inline-flex;
                    align-items: center;
                    gap: 7px;
                    transition: border-color 0.2s, color 0.2s, box-shadow 0.2s;
                  }}
                  button:hover {{
                    border-color: rgba(0,210,255,0.45);
                    color: #00d2ff;
                    box-shadow: 0 0 12px rgba(0,210,255,0.10);
                  }}
                  button svg {{ flex-shrink:0; }}
                  #feedback {{
                    font-family:'Plus Jakarta Sans',sans-serif;font-size:0.75rem;
                    color:#38f0b8;margin-top:6px;opacity:0;
                    transition:opacity 0.3s;
                  }}
                </style>
                <button onclick="doCopy()">
                  <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13"
                       viewBox="0 0 24 24" fill="none" stroke="currentColor"
                       stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                  </svg>
                  Copy Content
                </button>
                <div id="feedback">Copied to clipboard</div>
                <script>
                const TEXT = {repr(result)};
                function doCopy() {{
                  navigator.clipboard.writeText(TEXT).then(() => {{
                    const f = document.getElementById('feedback');
                    f.style.opacity = '1';
                    setTimeout(() => f.style.opacity = '0', 2200);
                  }});
                }}
                </script>
                """,
                height=68,
            )

        with col2:
            st.download_button(
                label="Download as .txt",
                data=result,
                file_name="generated_content.txt",
                mime="text/plain",
                use_container_width=True
            )