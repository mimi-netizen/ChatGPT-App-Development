import requests
import json
import base64
from pathlib import Path
from datetime import datetime
import os
from typing import Optional, List
import logging

class ImageGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-pro-vision"
        self.data_dir = Path.cwd() / "responses"
        self.image_dir = Path.cwd() / "images"
        self.setup_directories()
        self.setup_logging()

    def setup_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.data_dir.mkdir(exist_ok=True)
        self.image_dir.mkdir(exist_ok=True)

    def setup_logging(self) -> None:
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('image_generation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def generate_image(self, prompt: str, n: int = 1, size: str = "1024x1024") -> Optional[dict]:
        """
        Generate images using Gemini API.
        
        Args:
            prompt (str): The image generation prompt
            n (int): Number of images to generate
            size (str): Image size in format "widthxheight"
            
        Returns:
            Optional[dict]: API response containing generated images
        """
        try:
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            
            # Parse size string
            width, height = map(int, size.split('x'))
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.9,
                    "imageParams": {
                        "width": width,
                        "height": height,
                        "samples": n
                    }
                }
            }

            headers = {
                "Content-Type": "application/json"
            }

            self.logger.info(f"Generating {n} image(s) with prompt: {prompt}")
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            # Save raw response
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            response_file = self.data_dir / f"response_{timestamp}.json"
            with open(response_file, 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, indent=2)

            return response.json()

        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return None

    def save_images(self, response: dict, prompt: str) -> List[Path]:
        """
        Save generated images from API response.
        
        Args:
            response (dict): API response containing generated images
            prompt (str): Original prompt used for generation
            
        Returns:
            List[Path]: List of paths to saved images
        """
        saved_files = []
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            prompt_dir = self.image_dir / f"{prompt[:30]}_{timestamp}"
            prompt_dir.mkdir(exist_ok=True)

            for idx, image_data in enumerate(response.get("candidates", [])):
                try:
                    # Extract base64 image data from response
                    image_b64 = image_data["content"]["parts"][0]["image"]["data"]
                    
                    # Decode and save image
                    image_bytes = base64.b64decode(image_b64)
                    image_file = prompt_dir / f"image_{idx+1}.png"
                    
                    with open(image_file, 'wb') as f:
                        f.write(image_bytes)
                    
                    saved_files.append(image_file)
                    self.logger.info(f"Saved image to {image_file}")
                
                except (KeyError, ValueError) as e:
                    self.logger.error(f"Error processing image {idx+1}: {str(e)}")
                    continue

        except Exception as e:
            self.logger.error(f"Error saving images: {str(e)}")

        return saved_files

def main():
    # Initialize with your API key
    api_key = ""
    generator = ImageGenerator(api_key)

    # Example prompts
    prompts = [
        "3D render of a futuristic castle in a clear sky, digital art",
        "A photorealistic image of a peaceful garden with cherry blossoms",
        "An abstract painting of emotions using vibrant colors"
    ]

    for prompt in prompts:
        # Generate images
        response = generator.generate_image(
            prompt=prompt,
            n=2,  # Generate 2 images
            size="1024x1024"
        )

        if response:
            # Save generated images
            saved_files = generator.save_images(response, prompt)
            if saved_files:
                print(f"Successfully generated and saved {len(saved_files)} images for prompt: {prompt}")
                for file in saved_files:
                    print(f"- {file}")
            else:
                print(f"No images were saved for prompt: {prompt}")
        else:
            print(f"Failed to generate images for prompt: {prompt}")

if __name__ == "__main__":
    main()