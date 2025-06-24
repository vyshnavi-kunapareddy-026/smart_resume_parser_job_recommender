# summarizer.py (CPU-only version)

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "google/gemma-2b-it"

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it", use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it", use_auth_token=True)

summarizer = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=150,
    do_sample=True,
    temperature=0.7
)

def summarize_resume(layout_sections):
    prompt = f"""
    You are a resume summarizer. Based on the information below, write a 3–4 sentence professional summary of the candidate.

    Header: {layout_sections.get("header", "")}
    Summary/About: {layout_sections.get("about", "")}
    Education: {layout_sections.get("education", "")}
    Experience: {layout_sections.get("experience", "")}
    Skills: {layout_sections.get("skills", "")}
    Certifications: {layout_sections.get("additional_information", "")}

    Professional Summary:
    """
    output = summarizer(prompt)
    return output[0]["generated_text"].split("Professional Summary:")[-1].strip()
