"""
GEMINI FORGE - Ollama Client
Local AI integration for image analysis.
"""
import json
import base64
from pathlib import Path
from typing import Dict, Optional


# Try to import ollama
try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


# Local imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import OLLAMA_MODEL, OLLAMA_HOST, OLLAMA_ENABLED


def is_available() -> bool:
    """Check if Ollama is available and configured."""
    if not OLLAMA_ENABLED:
        return False
    if not OLLAMA_AVAILABLE:
        return False
    
    # Try to ping Ollama
    try:
        ollama.list()
        return True
    except Exception:
        return False


def load_image_base64(image_path: Path) -> str:
    """Load an image as base64 string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_quality(image_path: Path) -> Dict:
    """
    Analyze image quality using local vision model.
    
    Returns assessment of blur, artifacts, composition, etc.
    """
    if not is_available():
        return {
            "status": "unavailable",
            "error": "Ollama not available"
        }
    
    try:
        image_data = load_image_base64(image_path)
        
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{
                "role": "user",
                "content": """Analyze this image for quality. Rate each aspect 1-10:
1. Sharpness (is it blurry?)
2. Artifacts (compression, noise, glitches?)
3. Composition (is it well-framed?)
4. Color balance (natural colors?)
5. Overall quality

Respond in JSON format:
{
    "sharpness": X,
    "artifacts": X,
    "composition": X,
    "color_balance": X,
    "overall": X,
    "issues": ["list of specific issues if any"],
    "recommendation": "keep/upscale/regenerate"
}""",
                "images": [image_data]
            }]
        )
        
        # Try to parse as JSON
        try:
            result = json.loads(response["message"]["content"])
            result["status"] = "success"
            return result
        except json.JSONDecodeError:
            return {
                "status": "success",
                "raw_response": response["message"]["content"]
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def verify_content(image_path: Path, prompt: str) -> Dict:
    """
    Verify that an image matches its generation prompt.
    
    Returns assessment of prompt alignment.
    """
    if not is_available():
        return {
            "status": "unavailable",
            "error": "Ollama not available"
        }
    
    try:
        image_data = load_image_base64(image_path)
        
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{
                "role": "user",
                "content": f"""Compare this image to the prompt that was used to generate it.

PROMPT: "{prompt}"

Does the image match the prompt? Rate these aspects 1-10:
1. Subject match (correct character/object?)
2. Action match (doing the right thing?)
3. Style match (correct artistic style?)
4. Detail match (correct colors, props, etc?)

Respond in JSON format:
{{
    "subject_match": X,
    "action_match": X,
    "style_match": X,
    "detail_match": X,
    "overall_match": X,
    "missing": ["list what's missing from prompt"],
    "extra": ["list what's in image but not in prompt"],
    "verdict": "match/partial/mismatch"
}}""",
                "images": [image_data]
            }]
        )
        
        try:
            result = json.loads(response["message"]["content"])
            result["status"] = "success"
            return result
        except json.JSONDecodeError:
            return {
                "status": "success",
                "raw_response": response["message"]["content"]
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def suggest_upscale(image_path: Path) -> Dict:
    """
    Analyze if an image would benefit from upscaling.
    
    Returns recommendation and reasoning.
    """
    if not is_available():
        return {
            "status": "unavailable",
            "error": "Ollama not available"
        }
    
    try:
        image_data = load_image_base64(image_path)
        
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{
                "role": "user",
                "content": """Analyze this image to determine if it would benefit from AI upscaling.

Consider:
1. Current apparent resolution (low/medium/high?)
2. Level of detail present
3. Artifacts that upscaling might fix
4. Artifacts that upscaling might make worse

Respond in JSON format:
{
    "current_quality": "low/medium/high",
    "detail_level": "minimal/moderate/detailed",
    "upscale_benefit": 1-10,
    "upscale_risk": 1-10,
    "recommendation": "upscale/keep/regenerate",
    "reasoning": "brief explanation"
}""",
                "images": [image_data]
            }]
        )
        
        try:
            result = json.loads(response["message"]["content"])
            result["status"] = "success"
            return result
        except json.JSONDecodeError:
            return {
                "status": "success",
                "raw_response": response["message"]["content"]
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def describe_image(image_path: Path) -> str:
    """
    Get a description of an image.
    
    Useful for generating captions or verifying content.
    """
    if not is_available():
        return "Ollama not available"
    
    try:
        image_data = load_image_base64(image_path)
        
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{
                "role": "user",
                "content": "Describe this image in detail. Focus on: subject, action, style, colors, mood.",
                "images": [image_data]
            }]
        )
        
        return response["message"]["content"]
        
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Test the client
    print(f"Ollama available: {is_available()}")
    
    if is_available():
        print(f"Model: {OLLAMA_MODEL}")
        print("Ready for image analysis.")
    else:
        print("Ollama not available. Install with: pip install ollama")
        print("Make sure Ollama server is running: ollama serve")
