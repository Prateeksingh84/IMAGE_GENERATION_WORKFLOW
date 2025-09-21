import os
import json
from PIL import Image
from google import genai
from pathlib import Path
from dotenv import load_dotenv
from dataset_loader import download_images_dataset

# ----------------- CONFIG -----------------
OUTPUT_DIR = "outputs"
IMAGES_DIR = OUTPUT_DIR
LOGS_DIR = os.path.join(OUTPUT_DIR, "logs")
JSON_RESULTS = os.path.join(LOGS_DIR, "results.json")
EMAIL_BODY_HTML = os.path.join(LOGS_DIR, "email_body.html")
LOGO_PATH = "logo.png"
BRAND_COLOR = (0, 102, 204, 80)
IMAGE_SIZES = ["1024x1024", "2048x2048"]

# ----------------- LOAD API KEY -----------------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY missing in .env")

client = genai.Client(api_key=GOOGLE_API_KEY)

# ----------------- HELPERS -----------------
def ensure_dirs():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

def generate_image_from_prompt(prompt: str, size: str = "1024x1024"):
    if size not in ["1024x1024", "2048x2048"]:
        print(f"⚠️ Invalid size: {size}")
        return None
    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config={"image_size": size}
        )
        if not response.generated_images:
            return None
        return response.generated_images[0].image
    except Exception as e:
        print(f"❌ Google API error: {e}")
        return None

def apply_branding(img: Image.Image, logo_path=LOGO_PATH, brand_color=BRAND_COLOR):
    img = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, brand_color)
    img = Image.alpha_composite(img, overlay)
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        w, h = img.size
        logo_width = int(w * 0.15)
        logo_ratio = logo_width / logo.width
        logo_height = int(logo.height * logo_ratio)
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
        pos = (w - logo_width - 10, h - logo_height - 10)
        img.alpha_composite(logo, dest=pos)
    return img.convert("RGB")

# ----------------- MAIN WORKFLOW -----------------
def run_image_generation_workflow():
    ensure_dirs()
    
    # Get all dataset images
    image_files = download_images_dataset()

    results = []
    for idx, img_path in enumerate(image_files, start=1):
        # Use image filename as prompt for variation generation
        prompt = f"Generate a variation of the image: {os.path.basename(img_path)}"
        for size in IMAGE_SIZES:
            img = generate_image_from_prompt(prompt, size=size)
            if img:
                img = apply_branding(img)
                fname = f"img_{idx}_{size}.png"
                fpath = os.path.join(IMAGES_DIR, fname)
                img.save(fpath)
                results.append({"id": idx, "prompt": prompt, "size": size, "file_path": fpath})
            else:
                print(f"❌ Failed for {img_path}, size={size}")

    # Save JSON results
    with open(JSON_RESULTS, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    # HTML preview
    body = "<h2>Generated Images</h2><ul>"
    for r in results:
        body += f"<li><b>{r['prompt']} ({r['size']})</b><br><img src='{os.path.abspath(r['file_path'])}' width='300'></li>"
    body += "</ul>"
    with open(EMAIL_BODY_HTML, "w", encoding="utf-8") as f:
        f.write(body)

    print(f"✅ Done. {len(results)} images saved in {IMAGES_DIR}")
    return results, body

# ----------------- ENTRY POINT -----------------
if __name__ == "__main__":
    run_image_generation_workflow()
