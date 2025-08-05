# Calls external LLM API
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

LLM_MODEL = "mistralai/mixtral-8x7b-instruct"

def generate_answer(question, context):
    prompt = f"""You are a helpful assistant. Use the below context to answer the question.
    
    Context:
    {context}

    Question: {question}
    Answer:"""

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": "Answer only using the provided context."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()
