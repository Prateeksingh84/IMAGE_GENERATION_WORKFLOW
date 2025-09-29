import os
import json
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import google.generativeai as genai
from pathlib import Path

class BrandedImageGenerator:
    def __init__(self, config_path='config.json'):
        """Initialize the image generator with configuration"""
        self.load_config(config_path)
        self.setup_gemini()
        self.create_directories()
        
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.brand_colors = self.config['brand']['colors']
        self.output_dir = self.config['storage']['output_directory']
        self.logo_path = self.config['brand'].get('logo_path', None)
        
    def setup_gemini(self):
        """Setup Gemini API"""
        api_key = os.getenv('GEMINI_API_KEY') or self.config['api']['gemini_api_key']
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or config")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def create_directories(self):
        """Create necessary output directories"""
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        for size in self.config['image_variants']['sizes']:
            Path(f"{self.output_dir}/{size['name']}").mkdir(parents=True, exist_ok=True)
    
    def enhance_prompt_with_brand(self, user_prompt):
        """Enhance user prompt with brand guidelines"""
        brand_style = self.config['brand']['style_keywords']
        color_desc = f"using colors: {', '.join(self.brand_colors)}"
        
        enhanced_prompt = f"{user_prompt}, {brand_style}, {color_desc}, professional marketing image, high quality, detailed"
        return enhanced_prompt
    
    def generate_image_with_gemini(self, prompt):
        """Generate image using Gemini API (text description)"""
        try:
            # Note: Gemini's imagen capability through generative AI
            enhanced_prompt = self.enhance_prompt_with_brand(prompt)
            
            # For actual image generation, you'd use Imagen API
            # This is a placeholder that creates a colored base image
            # In production, replace with actual Gemini Imagen API call
            
            print(f"Generating image with prompt: {enhanced_prompt}")
            
            # Create base image (placeholder - replace with actual API call)
            img = self.create_base_image(enhanced_prompt)
            return img
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def create_base_image(self, prompt):
        """Create a base image with brand colors (placeholder for actual generation)"""
        # This creates a gradient with brand colors as a placeholder
        # Replace this with actual Gemini Imagen API call
        
        width, height = 1024, 1024
        img = Image.new('RGB', (width, height), color=self.brand_colors[0])
        draw = ImageDraw.Draw(img)
        
        # Create gradient effect
        for i in range(height):
            color_val = int(255 * (i / height))
            draw.line([(0, i), (width, i)], fill=self.brand_colors[0])
        
        # Add prompt text as overlay
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Add text
        text = "Generated Image"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        draw.text((x, y), text, fill='white', font=font)
        
        return img
    
    def apply_branding(self, img):
        """Apply logo overlay and brand elements"""
        if not self.logo_path or not os.path.exists(self.logo_path):
            return img
        
        try:
            logo = Image.open(self.logo_path).convert('RGBA')
            
            # Resize logo to 10% of image width
            logo_width = img.width // 10
            logo_ratio = logo_width / logo.width
            logo_height = int(logo.height * logo_ratio)
            logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
            # Position logo in bottom right corner
            position = (img.width - logo_width - 20, img.height - logo_height - 20)
            
            # Create a copy to paste logo
            img_copy = img.copy().convert('RGBA')
            img_copy.paste(logo, position, logo)
            
            return img_copy.convert('RGB')
        except Exception as e:
            print(f"Error applying logo: {e}")
            return img
    
    def generate_variants(self, base_image, prompt_name):
        """Generate multiple size variants of the image"""
        variants = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for size_config in self.config['image_variants']['sizes']:
            name = size_config['name']
            width = size_config['width']
            height = size_config['height']
            
            # Resize image
            resized_img = base_image.resize((width, height), Image.Resampling.LANCZOS)
            
            # Generate filename
            filename = f"{prompt_name}_{name}_{timestamp}.{self.config['image_variants']['format']}"
            filepath = os.path.join(self.output_dir, name, filename)
            
            # Save image
            resized_img.save(filepath, quality=95)
            
            variants.append({
                'name': name,
                'size': f"{width}x{height}",
                'path': filepath,
                'url': f"file://{os.path.abspath(filepath)}"
            })
            
            print(f"Saved {name} variant: {filepath}")
        
        return variants
    
    def process_prompt(self, prompt, prompt_name=None):
        """Process a single prompt and generate branded images"""
        if not prompt_name:
            prompt_name = prompt.replace(' ', '_')[:30]
        
        print(f"\n{'='*60}")
        print(f"Processing prompt: {prompt}")
        print(f"{'='*60}\n")
        
        # Generate base image
        base_image = self.generate_image_with_gemini(prompt)
        if not base_image:
            print("Failed to generate image")
            return None
        
        # Apply branding
        branded_image = self.apply_branding(base_image)
        
        # Generate variants
        variants = self.generate_variants(branded_image, prompt_name)
        
        result = {
            'prompt': prompt,
            'timestamp': datetime.now().isoformat(),
            'variants': variants
        }
        
        return result
    
    def batch_process(self, prompts):
        """Process multiple prompts"""
        results = []
        
        for i, prompt_data in enumerate(prompts, 1):
            if isinstance(prompt_data, dict):
                prompt = prompt_data['prompt']
                name = prompt_data.get('name', f"prompt_{i}")
            else:
                prompt = prompt_data
                name = f"prompt_{i}"
            
            result = self.process_prompt(prompt, name)
            if result:
                results.append(result)
        
        return results
    
    def send_notification(self, results):
        """Send completion notification"""
        notification_config = self.config.get('notification', {})
        
        if not notification_config.get('enabled', False):
            print("\nNotifications disabled")
            return
        
        # Prepare notification message
        message = "Image Generation Complete!\n\n"
        for result in results:
            message += f"Prompt: {result['prompt']}\n"
            message += f"Generated at: {result['timestamp']}\n"
            message += "Variants:\n"
            for variant in result['variants']:
                message += f"  - {variant['name']}: {variant['url']}\n"
            message += "\n"
        
        print(f"\n{'='*60}")
        print("NOTIFICATION")
        print(f"{'='*60}")
        print(message)
        
        # If webhook URL is provided, send POST request
        webhook_url = notification_config.get('webhook_url')
        if webhook_url:
            try:
                response = requests.post(webhook_url, json={
                    'message': message,
                    'results': results
                })
                print(f"Webhook notification sent: {response.status_code}")
            except Exception as e:
                print(f"Error sending webhook: {e}")


def main():
    """Main execution function"""
    print("="*60)
    print("BRANDED IMAGE GENERATION WORKFLOW")
    print("="*60)
    
    # Initialize generator
    generator = BrandedImageGenerator('config.json')
    
    # Sample prompts for testing
    sample_prompts = [
        {
            'name': 'summer_sale',
            'prompt': 'Summer sale promotion with beach vibes and tropical elements'
        },
        {
            'name': 'product_launch',
            'prompt': 'Modern tech product launch with futuristic design'
        },
        {
            'name': 'social_media',
            'prompt': 'Engaging social media post with dynamic composition'
        },
        {
            'name': 'email_header',
            'prompt': 'Professional email header with clean corporate aesthetic'
        },
        {
            'name': 'web_banner',
            'prompt': 'Eye-catching web banner with bold typography'
        }
    ]
    
    # Process all prompts
    results = generator.batch_process(sample_prompts)
    
    # Send notification
    generator.send_notification(results)
    
    print(f"\n{'='*60}")
    print(f"Processing complete! Generated {len(results)} image sets")
    print(f"Output directory: {generator.output_dir}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
