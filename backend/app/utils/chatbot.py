# app/utils/chatbot.py

from transformers import pipeline

# Initialize lightweight summarizer or instruction model
llm = pipeline("text-generation", model="google/flan-t5-small", tokenizer="google/flan-t5-small")

def resume_chatbot(question: str, resume_context: dict):
    context = "\n".join([f"{k.upper()}: {v}" for k, v in resume_context.items()])
    prompt = f"Based on this resume:\n{context}\n\nAnswer this question: {question}"

    result = llm(prompt, max_length=256, do_sample=True)[0]["generated_text"]
    return result.strip()
