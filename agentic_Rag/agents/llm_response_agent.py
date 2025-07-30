import requests
from agents.ingestion_agent import create_mcp_message

import os
from dotenv import load_dotenv
load_dotenv()

# Use HuggingFace inference API (free for public models)
API_URL = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json"
}


def call_llm(prompt):
    response = requests.post(API_URL, headers=headers, json={
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    })

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"[Error] LLM call failed: {response.status_code} - {response.text}"



def build_prompt(query, context_chunks):
    context_str = "\n\n".join(context_chunks)
    prompt = f"""You are a helpful assistant.

Use the following context to answer the user's question.

Context:
{context_str}

Question:
{query}

Answer:"""
    return prompt


def generate_response_mcp(mcp_message):
    query = mcp_message["payload"]["query"]
    chunks = mcp_message["payload"]["top_chunks"]

    prompt = build_prompt(query, chunks)
    answer = call_llm(prompt)

    return create_mcp_message(
        sender="LLMResponseAgent",
        receiver="UI",
        trace_id=mcp_message["trace_id"],
        msg_type="FINAL_ANSWER",
        payload={
            "answer": answer,
            "source_chunks": chunks,
            "query": query
        }
    )
