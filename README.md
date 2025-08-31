# AI Content Creation Assistant (Open-Source)

This project is a self-contained Streamlit app demonstrating a Generative AI Content Assistant using:
- Streamlit (frontend)
- LangChain + Groq (LLM provider)
- LangGraph (workflow)
- LangChain memory (session memory)
- Optional image generation (Stable Diffusion via diffusers or remote APIs)

## Features included
- Prompt handling with style parameters (tone, format, length)
- Multi-turn conversation with session memory
- Prompt templates for blog / tweet / email / marketing copy
- LangGraph workflow (preprocess -> llm -> postprocess)
- Image generation module supporting:
  - Local Stable Diffusion (diffusers) (requires GPU + torch)
  - Remote API usage (Stability.ai, Replicate) placeholders
- Example VS Code launch config & .env.example

## How to run (developer)
1. Install Python 3.10 or 3.11
2. Create virtualenv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in keys (GROQ_API_KEY, optional STABILITY_API_KEY, REPLICATE_API_TOKEN)
5. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Notes
- Local image generation requires a compatible CUDA-enabled GPU and matching `torch` build. If you don't have GPU, use remote APIs.
- This repo contains placeholder model names such as `llama-3.3-70b-versatile`. Ensure your Groq account has access and quotas for chosen models.

## Files of interest
- `app.py` — Streamlit frontend
- `core/llm_client.py` — LangChain + Groq wrapper + prompt preprocessing
- `core/graph_workflow.py` — LangGraph example
- `core/prompts.py` — Prompt templates
- `core/image_gen.py` — Image generation helpers (local & remote)
- `requirements.txt` — Python dependencies

## Image models integrated

This scaffold now includes direct support for:

- Stable Diffusion (via Hugging Face `diffusers` StableDiffusionPipeline or DiffusionPipeline auto-detection)
- Kandinsky models (via `diffusers` pipelines; use a Kandinsky model ID such as `kandinsky-community/kandinsky-3` or `kandinsky-community/kandinsky-2-2`)

Set `DEFAULT_IMAGE_MODEL` in `.env` to one of your chosen model IDs (e.g. `stabilityai/stable-diffusion-2-1` or `kandinsky-community/kandinsky-3`).

**Important:** Large models require GPU and HF authentication tokens for private models. If you need help setting HF tokens, set `HF_TOKEN` in your `.env`.


## Hugging Face Inference API

If you don't have a local GPU, set `HF_TOKEN` (Hugging Face API token) in your `.env` and the app will use the Hugging Face Inference API to generate images for the selected model id. Example model ids: `stabilityai/stable-diffusion-2-1`, `runwayml/stable-diffusion-v1-5`, `kandinsky-community/kandinsky-3`.
"# AI-Content-Creation-Assistant" 
