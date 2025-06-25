from transformers import pipeline

# Use FLAN-T5-small for QA-style completion
llm = pipeline("text2text-generation", model="google/flan-t5-small", tokenizer="google/flan-t5-small")

def format_resume_context(layout: dict) -> str:
    """
    Create a clean, readable text version of the resume layout.
    """
    sections = layout.get("parsed", {}).get("layout_sections", {})
    formatted = []

    for section, content in sections.items():
        if content:
            formatted.append(f"{section.capitalize()}:\n{content.strip()}")

    return "\n\n".join(formatted)

def resume_chatbot(question: str, resume_context: dict) -> str:
    context_text = format_resume_context(resume_context)
    prompt = f"{context_text}\n\nQuestion: {question}\nAnswer:"

    result = llm(prompt, max_length=256, do_sample=False, temperature=0.3)[0]["generated_text"]

    # Strip the prompt from the start if model echoes it
    if "Answer:" in result:
        return result.split("Answer:", 1)[-1].strip()
    return result.strip()
