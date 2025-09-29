import os
import json
from pathlib import Path

def create_config():
    """Create config.json file"""
    config = {
        "api": {
            "gemini_api_key": "YOUR_GEMINI_API_KEY_HERE"
        },
        "brand": {
            "name": "TechBrand Inc.",
            "colors": [
                "#0066CC",
                "#00A3E0",
                "#FFFFFF"
            ],
            "style_keywords": "modern, clean, professional, minimalist",
            "logo_path": "assets/logo.png"
        },
        "image_variants": {
            "format": "jpg",
            "sizes": [
                {
                    "name": "social_square",
                    "width": 1080,
                    "height": 1080,
                    "description": "Instagram/Facebook square post"
                },
                {
                    "name": "social_story",
                    "width": 1080,
                    "height": 1920,
                    "description": "Instagram/Facebook story"
                },
                {
                    "name": "web_banner",
                    "width": 1920,
                    "height": 1080,
                    "description": "Website banner/hero image"
                },
                {
                    "name": "email_header",
                    "width": 600,
                    "height": 200,
                    "description": "Email header image"
                },
                {
                    "name": "thumbnail",
                    "width": 400,
                    "height": 400,
                    "description": "Thumbnail/preview"
                }
            ]
        },
        "storage": {
            "output_directory": "generated_images",
            "organize_by_date": True
        },
        "notification": {
            "enabled": True,
            "webhook_url": "",
            "email": ""
        }
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("✅ Created config.json")

def create_env_file():
    """Create .env file"""
    env_content = """# Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Webhook URL for notifications
WEBHOOK_URL=https://your-webhook-url.com/notify
"""
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Created .env file")

def create_directories():
    """Create necessary directories"""
    dirs = [
        'assets',
        'generated_images',
        'generated_images/social_square',
        'generated_images/social_story',
        'generated_images/web_banner',
        'generated_images/email_header',
        'generated_images/thumbnail'
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    print("✅ Created directories")

def create_placeholder_logo():
    """Create a simple placeholder logo"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple logo
        img = Image.new('RGBA', (200, 200), color=(0, 102, 204, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a circle
        draw.ellipse([20, 20, 180, 180], fill=(0, 102, 204, 255))
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        text = "TB"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (200 - text_width) // 2
        y = (200 - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        
        # Save
        img.save('assets/logo.png')
        print("✅ Created placeholder logo (assets/logo.png)")
    except Exception as e:
        print(f"⚠️  Could not create logo: {e}")
        print("   You can add your own logo to assets/logo.png later")

def main():
    print("="*60)
    print("SETTING UP IMAGE GENERATION WORKFLOW")
    print("="*60)
    print()
    
    # Check if files already exist
    if os.path.exists('config.json'):
        response = input("config.json already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Skipping config.json")
        else:
            create_config()
    else:
        create_config()
    
    if os.path.exists('.env'):
        response = input(".env already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Skipping .env")
        else:
            create_env_file()
    else:
        create_env_file()
    
    # Always create directories
    create_directories()
    
    # Create placeholder logo if it doesn't exist
    if not os.path.exists('assets/logo.png'):
        create_placeholder_logo()
    else:
        print("✅ Logo already exists")
    
    print()
    print("="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    print()
    print("Next Steps:")
    print("1. Edit config.json and add your GEMINI_API_KEY")
    print("   OR set GEMINI_API_KEY in .env file")
    print()
    print("2. (Optional) Replace assets/logo.png with your brand logo")
    print()
    print("3. Run the program:")
    print("   python main.py")
    print()
    print("Get Gemini API Key from: https://makersuite.google.com/app/apikey")
    print("="*60)

if __name__ == "__main__":
    main()
