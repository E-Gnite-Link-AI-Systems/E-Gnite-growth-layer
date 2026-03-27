import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_outreach(lead):
    prompt = f"""
Write a short professional outreach message.

Name: {lead['name']}
Company: {lead['company']}
Industry: {lead.get('industry', 'business')}

Goal: Offer growth services and ask for a call.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
