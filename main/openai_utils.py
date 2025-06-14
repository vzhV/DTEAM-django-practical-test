import openai
from django.conf import settings

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

def gpt_translate(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content.strip()