# Image Generation Workflow

A Python-based workflow to generate AI-powered images using **Google Gen AI** and Kaggle datasets. This project automatically downloads datasets, generates variations of images, applies branding, and saves the results in an organized format.

---

## 🚀 Features

- Automatically downloads datasets from Kaggle using `kagglehub`.
- Supports image variation generation using **Google Gen AI (`imagen-4.0-generate-001`)**.
- Applies branding overlay and logo to generated images.
- Saves generated images, JSON logs, and HTML previews.
- Fully configurable image sizes (`1024x1024` or `2048x2048`).

---

## 📦 Requirements

- Python 3.9+
- Libraries:
  - `pandas`
  - `Pillow`
  - `python-dotenv`
  - `kagglehub`
  - `google-genai` (or `google` if using their Gen AI SDK)

---

## ⚙️ Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/image-generation-workflow.git
cd image-generation-workflow
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the project root with your Google API key:
```ini
GOOGLE_API_KEY=your_google_genai_api_key
```

4. **Optional: Add logo for branding**
Place a logo file named `logo.png` in the project root (used for overlay on generated images).

---

## 📂 Usage

**Run the main workflow:**
```bash
python main.py
```

The workflow will:
- Download the Kaggle dataset (`pavansanagapati/images-dataset`) automatically.
- Generate variations of each image using Google Gen AI.
- Apply branding overlay and logo.
- Save outputs in `outputs/`:
  - `outputs/*.png` → Generated images
  - `outputs/logs/results.json` → JSON log of images
  - `outputs/logs/email_body.html` → HTML preview of images

---

## ⚙️ Configuration

You can configure the following variables in `main.py`:

| Variable | Description |
|----------|-------------|
| `OUTPUT_DIR` | Directory to save images and logs |
| `IMAGE_SIZES` | List of sizes for generation (`1024x1024`, `2048x2048`) |
| `LOGO_PATH` | Path to logo for branding overlay |
| `BRAND_COLOR` | RGBA color overlay applied on images |

---

## 📁 Project Structure

```
image-generation-workflow/
│
├─ dataset_loader.py      # Downloads Kaggle dataset and provides image paths
├─ main.py                # Main workflow to generate images
├─ .env                   # Environment variables (API keys)
├─ outputs/               # Generated images and logs
│   ├─ logs/
│   │   ├─ results.json
│   │   └─ email_body.html
│   └─ *.png
└─ README.md
```

---

## ⚠️ Notes

- Ensure your Google API key has access to the `imagen-4.0-generate-001` model.
- The Kaggle dataset is downloaded automatically; no CSV or prompts file is required.
- The project currently supports only image generation from filenames as prompts. Image-to-image variation can be added as a future enhancement.

---

## 📌 License

This project is open-source and available under the MIT License.
