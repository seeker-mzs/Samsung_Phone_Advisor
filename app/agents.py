import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def review_generator(phone1, phone2=None):

    if phone2:
        prompt = f"""
        Compare these phones:

        Phone 1:
        {phone1.__dict__}

        Phone 2:
        {phone2.__dict__}

        Focus on photography and battery.
        Recommend one.
        """
    else:
        prompt = f"""
        Generate a review and recommendation for:
        {phone1.__dict__}
        """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]