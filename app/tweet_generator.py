from utils.helpers import generate_content


def generate_tweet(topic, tone):

    prompt = f"""
    You are a viral social media strategist.

    Write a highly engaging tweet.

    Topic: {topic}
    Tone: {tone}

    Rules:
    - Maximum 280 characters
    - Use engaging hooks
    - Add emojis if relevant
    - Make it shareable
    """


    return generate_content(prompt)
