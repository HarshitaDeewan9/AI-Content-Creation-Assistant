import os
import streamlit as st
from dotenv import load_dotenv
from core.graph_workflow import build_compiled_graph
from core.prompts import PROMPT_TEMPLATES
from core.image_gen import generate_image

load_dotenv()

st.set_page_config(page_title="AI Content Creation Assistant", layout="centered")
st.title("AI Content Creation Assistant")

with st.sidebar:
    st.header("Settings")
    model = st.selectbox("Text model", [os.getenv("DEFAULT_TEXT_MODEL", "llama-3.3-70b-versatile")])
    tone = st.selectbox("Tone", ["Neutral", "Formal", "Casual", "Funny", "Professional"], index=0)
    fmt = st.selectbox("Format", ["Article", "Blog", "Tweet", "Email", "Bullet Points", "Marketing"], index=1)
    length = st.selectbox("Length", ["Short", "Medium", "Long"], index=1)
    use_image = st.checkbox("Generate image with content", value=False)
    if use_image:
        img_model = st.text_input("Image model id (Hugging Face)", value=os.getenv("DEFAULT_IMAGE_MODEL", "black-forest-labs/FLUX.1-dev"))

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Quick templates")
cols = st.columns(4)
for i, key in enumerate(list(PROMPT_TEMPLATES.keys())[:4]):
    if cols[i].button(key):
        st.session_state.prefill = PROMPT_TEMPLATES[key]

prompt = st.text_area("Prompt", value=st.session_state.get("prefill", ""), height=140)
submit = st.button("Generate")

if submit and prompt.strip():
    st.session_state.history.append(("user", prompt))
    graph = build_compiled_graph()
    # Build chat history text
    chat_context = ""
    for role, msg in st.session_state.history:
        if role == "user":
            chat_context += f"User: {msg}\n"
        elif role == "assistant":
            chat_context += f"Assistant: {msg}\n"

    # Prepend history to current prompt
    full_prompt = f"{chat_context}\nUser: {prompt}\nAssistant:"

    input_state = {
        "user_prompt": full_prompt,
        "style": {"tone": tone, "format": fmt, "length": length},
    }
    result = graph.invoke(input_state)

    assistant_text = result.get("response", "<no response>")
    st.session_state.history.append(("assistant", assistant_text))

    if use_image:
        img_prompt = f"{prompt}\n\nSummary: {assistant_text[:300]}"
        model_name = img_model if 'img_model' in locals() else os.getenv('DEFAULT_IMAGE_MODEL')
        image_path = generate_image(img_prompt, model_name, output_dir='outputs', filename_prefix='gen')
        if image_path:
            st.session_state.history.append(('assistant_image', image_path))
        else:
            st.session_state.history.append(('assistant', '⚠️ Image generation failed. Check HF_TOKEN and model id.'))

for role, text in st.session_state.history:
    if role == "user":
        st.chat_message("user").write(text)
    elif role == "assistant":
        st.chat_message("assistant").write(text)
    elif role == "assistant_image":
        st.image(text, caption="Generated image")

st.markdown("---")
st.caption("Built by Harshita Deewan")