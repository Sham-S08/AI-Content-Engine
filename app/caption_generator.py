from utils.helpers import generate_content


def generate_caption(topic, tone):

    prompt = f"""
    You are an Instagram growth strategist.

    Write an engaging Instagram caption.

    Topic: {topic}
    Tone: {tone}

    Requirements:
    - Engaging hook
    - Emojis
    - 5-8 relevant hashtags
    """


    return generate_content(prompt)
