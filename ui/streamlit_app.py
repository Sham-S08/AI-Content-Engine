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
    page_icon="🚀",
    layout="centered"
)

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.title("🕘 Content History")

if st.session_state.history:
    for item in reversed(st.session_state.history):
        with st.sidebar.expander(f"{item['type']} • {item['topic']}"):
            st.write(item["content"])
else:
    st.sidebar.write("No content generated yet.")

if st.sidebar.button("Clear History"):
    st.session_state.history = []

st.title("🚀 AI Content Engine")

st.markdown(
"""
Generate high-quality **blogs, tweets, captions, and LinkedIn posts**
using AI powered by Gemini.
"""
)

content_type = st.selectbox(
    "Select Content Type",
    ["Blog Post", "Tweet", "Instagram Caption", "LinkedIn Post"]
)

topic = st.text_input("Enter Topic")

user_style = None
if content_type == "LinkedIn Post":
    user_style = st.text_area(
        "Optional: Paste a sample of your LinkedIn post style",
        placeholder="Example:\n🌟 I'm excited to share...\n\nKey insights:\n1️⃣ ...\n2️⃣ ...\n\n#AI #Tech"
    )

tone = st.selectbox(
    "Select Tone",
    ["Professional", "Casual", "Funny", "Motivational", "Inspirational"]
)

generate = st.button("Generate Content")

if generate:

    if not topic:
        st.warning("Please enter a topic.")

    else:
        with st.spinner("Generating content..."):

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

        st.subheader("Generated Content")
        st.write(result)

        components.html(
            f"""
            <textarea id="copyText" style="width:100%; height:150px;">{result}</textarea>
            <button onclick="copyText()" style="margin-top:8px;padding:8px 12px;border:none;background:#4CAF50;color:white;border-radius:6px;">
            📋 Copy Content
            </button>

            <script>
            function copyText() {{
                var copyText = document.getElementById("copyText");
                copyText.select();
                copyText.setSelectionRange(0, 99999);
                navigator.clipboard.writeText(copyText.value);
                alert("Content copied!");
            }}
            </script>
            """,
            height=220,
        )

        st.download_button(
            label="Download Content",
            data=result,
            file_name="generated_content.txt",
            mime="text/plain"
        )

