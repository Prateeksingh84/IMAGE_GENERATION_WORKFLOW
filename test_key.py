import os
from dotenv import load_dotenv
import google.generativeai as genai
import base64
from PIL import Image
import io

load_dotenv()
GOOGLE_API_KEY = os.getenv("AIzaSyC0lseA1GCiwOPJmPV5RYWY1CBWflXogGI")

if not GOOGLE_API_KEY:
    raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in .env")

genai.configure(api_key=GOOGLE_API_KEY)

prompt = "Minimalist advertisement for a luxury watch"
response = genai.generate_image(
    model="imagen-2.0",
    prompt=prompt,
    size="512x512"
)

# Save image
img_data = base64.b64decode(response.images[0])
img = Image.open(io.BytesIO(img_data))
img.save("outputs/images/test_watch.png")
img.show()
print("✅ Image generated successfully with Google API")
