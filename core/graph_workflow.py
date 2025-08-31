from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from core.llm_client import generate_text_with_langchain

class ChatState(TypedDict):
    user_prompt: str
    style: dict
    response: str

def node_preprocess(state: ChatState) -> dict:
    style = state.get("style") or {}
    # minimal sanitization
    user_prompt = state.get("user_prompt","").strip()
    return {"user_prompt": user_prompt, "style": style}

def node_llm(state: ChatState) -> dict:
    prompt = state["user_prompt"]
    style = state["style"]
    # call LLM
    out = generate_text_with_langchain(prompt, style)
    return {"response": str(out)}

def node_postprocess(state: ChatState) -> dict:
    resp = state.get("response", "")
    # simple postprocessing: trim
    return {"response": resp.strip()}

def build_compiled_graph():
    workflow = StateGraph(ChatState)
    workflow.add_node("pre", node_preprocess)
    workflow.add_node("llm", node_llm)
    workflow.add_node("post", node_postprocess)

    workflow.add_edge(START, "pre")
    workflow.add_edge("pre", "llm")
    workflow.add_edge("llm", "post")
    workflow.add_edge("post", END)

    compiled = workflow.compile()
    return compiled