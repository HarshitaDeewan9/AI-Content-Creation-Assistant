from dotenv import load_dotenv
import os
from typing import Dict
load_dotenv()

try:
    from langchain_groq import ChatGroq
    from langchain.prompts import (
        ChatPromptTemplate,
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate,
    )
except Exception as e:
    raise ImportError("Please install langchain-groq and langchain. See requirements.txt") from e

def get_llm(model: str = None, temperature: float = 0.2):
    model = model or os.getenv("DEFAULT_TEXT_MODEL", "llama-3.3-70b-versatile")
    return ChatGroq(model=model, temperature=temperature)

def build_system_instructions(style: Dict) -> str:
    tone = style.get("tone", "neutral")
    fmt = style.get("format", "article")
    length = style.get("length", "medium")
    instructions = (
        "You are an expert content assistant. "
        f"Tone: {tone}. Output format: {fmt}. Desired length: {length}."
        " If the user asks for structure, obey it. Return clean text only."
    )
    return instructions

def generate_text_with_langchain(prompt: str, style: Dict, model: str = None):
    llm = get_llm(model=model)
    system_template = SystemMessagePromptTemplate.from_template(build_system_instructions(style))
    human_template = HumanMessagePromptTemplate.from_template("{user_input}")
    chat_prompt = ChatPromptTemplate.from_messages([system_template, human_template])
    messages = chat_prompt.format_messages(user_input=prompt)
    outputs = llm.invoke(messages)
    # attempt to normalize output to string
    out = outputs.content
    try:
        return str(out)
    except:
        # fallback: inspect for attributes
        if hasattr(out, "content"):
            return out.content
        return repr(out)