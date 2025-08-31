import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
DEFAULT_IMAGE_MODEL = os.getenv("DEFAULT_IMAGE_MODEL", "black-forest-labs/FLUX.1-dev")

API_URL_TEMPLATE = "https://api-inference.huggingface.co/models/{model_id}"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate_image(prompt: str, model_id: str = None, output_dir: str = "outputs", filename_prefix: str = "gen"):
    """
    Generate an image using Hugging Face Inference API.

    Args:
        prompt (str): The text prompt for image generation
        model_id (str): Hugging Face model id (default from .env if None)
        output_dir (str): Directory where the image will be saved
        filename_prefix (str): Prefix for the output file name

    Returns:
        str: Path to the saved image, or None if failed
    """
    if model_id is None:
        model_id = DEFAULT_IMAGE_MODEL

    if not HF_TOKEN:
        raise ValueError("HF_TOKEN not found. Please set it in your .env file.")

    api_url = API_URL_TEMPLATE.format(model_id=model_id)

    print(f"🔗 Calling API: {api_url}")
    print(f"🪪 Using Token: {'SET' if HF_TOKEN else 'MISSING'}")
    print(f"🎨 Prompt: {prompt}")

    payload = {"inputs": prompt}

    response = requests.post(api_url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{filename_prefix}_{timestamp}.png")
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Image saved to {output_path}")
        return output_path
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        return None