from utils.helpers import generate_content


def generate_blog(topic, tone):

    prompt = f"""
    You are an expert content writer and SEO strategist.

    Write a high-quality SEO optimized blog post.

    Topic: {topic}
    Tone: {tone}

    Requirements:
    - Catchy SEO-friendly title
    - Engaging introduction
    - 3-4 detailed sections with headings
    - Practical insights or examples
    - Strong conclusion
    - Maintain readability and flow
    """


    return generate_content(prompt)
