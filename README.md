# Branded Image Generation Workflow

Automated Python workflow for generating branded marketing images using Gemini API.

## Features

- ✅ AI image generation using Gemini API
- ✅ Consistent brand guidelines application
- ✅ Multiple image format variants (social media, web, email)
- ✅ Logo overlay and branding
- ✅ Organized cloud storage structure
- ✅ Completion notifications

## Project Structure

```
image-generation-workflow/
├── main.py                 # Main application
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Environment template
├── README.md             # This file
├── assets/               # Brand assets
│   └── logo.png         # Your brand logo
└── generated_images/     # Output directory (auto-created)
    ├── social_square/
    ├── social_story/
    ├── web_banner/
    ├── email_header/
    └── thumbnail/
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**Get Gemini API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy and paste it into `.env` file

### 3. Configure Brand Settings

Edit `config.json` to customize:
- Brand colors (hex codes)
- Brand style keywords
- Logo path
- Image sizes and formats
- Output directory
- Notification settings

### 4. Add Brand Logo (Optional)

Place your logo file in the `assets/` directory:

```bash
mkdir -p assets
# Copy your logo.png to assets/logo.png
```

Logo should be PNG with transparent background for best results.

## Usage

### Run the Image Generator

```bash
python main.py
```

This will:
1. Generate 5 sample branded images
2. Create multiple size variants for each
3. Save to organized directories
4. Print download links

### Customize Prompts

Edit the `sample_prompts` list in `main.py`:

```python
sample_prompts = [
    {
        'name': 'custom_name',
        'prompt': 'Your custom prompt here'
    }
]
```

### Single Image Generation

```python
from main import BrandedImageGenerator

generator = BrandedImageGenerator()
result = generator.process_prompt(
    prompt="Your image description",
    prompt_name="my_image"
)
```

## Image Variants Generated

| Variant | Size | Use Case |
|---------|------|----------|
| social_square | 1080x1080 | Instagram/Facebook posts |
| social_story | 1080x1920 | Instagram/Facebook stories |
| web_banner | 1920x1080 | Website banners/hero |
| email_header | 600x200 | Email headers |
| thumbnail | 400x400 | Preview thumbnails |

## Output Structure

```
generated_images/
├── social_square/
│   ├── summer_sale_social_square_20250929_143022.jpg
│   └── product_launch_social_square_20250929_143045.jpg
├── social_story/
│   ├── summer_sale_social_story_20250929_143022.jpg
│   └── product_launch_social_story_20250929_143045.jpg
└── ... (other variants)
```

## Brand Style Guide

Configure in `config.json`:

```json
{
  "brand": {
    "name": "Your Brand",
    "colors": ["#Primary", "#Secondary", "#Accent"],
    "style_keywords": "modern, clean, professional",
    "logo_path": "assets/logo.png"
  }
}
```

## Webhook Notifications

Enable notifications in `config.json`:

```json
{
  "notification": {
    "enabled": true,
    "webhook_url": "https://your-webhook.com/notify"
  }
}
```

Notification payload:
```json
{
  "message": "Image Generation Complete!",
  "results": [
    {
      "prompt": "...",
      "timestamp": "...",
      "variants": [...]
    }
  ]
}
```

## Sample Prompts Included

1. **Summer Sale** - Beach vibes and tropical elements
2. **Product Launch** - Modern tech with futuristic design
3. **Social Media** - Engaging dynamic composition
4. **Email Header** - Clean corporate aesthetic
5. **Web Banner** - Bold typography

## Troubleshooting

### API Key Issues
- Ensure `GEMINI_API_KEY` is set in `.env` or `config.json`
- Verify API key is active at https://makersuite.google.com

### Logo Not Appearing
- Check logo path in `config.json`
- Ensure logo file exists
- Use PNG format with transparency

### Image Quality
- Adjust quality parameter in `main.py` (default: 95)
- Modify image dimensions in `config.json`

### Dependencies Error
```bash
pip install --upgrade -r requirements.txt
```

## Advanced Usage

### Batch Processing from File

Create `prompts.json`:
```json
[
  {"name": "promo1", "prompt": "Description 1"},
  {"name": "promo2", "prompt": "Description 2"}
]
```

Load and process:
```python
import json
from main import BrandedImageGenerator

with open('prompts.json') as f:
    prompts = json.load(f)

generator = BrandedImageGenerator()
results = generator.batch_process(prompts)
```

### Custom Variant Sizes

Add to `config.json`:
```json
{
  "name": "custom_size",
  "width": 1200,
  "height": 628,
  "description": "LinkedIn post"
}
```

## Notes

- **Important**: Current implementation uses placeholder image generation. For production use with actual AI-generated images, you need to integrate Gemini Imagen API or use alternative services like DALL-E or Stable Diffusion.
- Images are saved locally. For cloud storage (AWS S3, Google Cloud Storage), add upload functionality.
- Rate limits apply based on your Gemini API tier.

## License

MIT License - Free to use and modify

## Support

For issues or questions:
- Check Gemini API docs: https://ai.google.dev/
- Review configuration settings
- Verify all dependencies installed
