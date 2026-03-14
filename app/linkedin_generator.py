from utils.helpers import generate_content


def generate_linkedin_post(topic, tone, user_style=None):

    if user_style:
        prompt = f"""
            You are a professional LinkedIn content creator.

            Write a LinkedIn post about:

            Topic: {topic}
            Tone: {tone}

            Follow this user's posting style:

            {user_style}

            Maintain the same structure and formatting.
            Add relevant hashtags at the end.
            """

    else:
        prompt = f"""
            You are a professional LinkedIn content creator.

            Write a high-quality LinkedIn post.

            Topic: {topic}
            Tone: {tone}

            Structure:
            - Strong hook
            - Short paragraphs
            - Bullet points if useful
            - Call to action
            - 4-6 relevant hashtags
            """

    return generate_content(prompt)
