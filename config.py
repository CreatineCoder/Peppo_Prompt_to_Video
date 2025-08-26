import os
from enum import Enum
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class VideoProvider(Enum):
    STABILITY_AI = "stability_ai"

class Config:
    # API Configuration
    DEFAULT_PROVIDER = VideoProvider.STABILITY_AI
    
    # Load API keys from environment variables
    STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")
    
    # Video Generation Settings
    DEFAULT_DURATION = 7
    MIN_DURATION = 5
    MAX_DURATION = 10
    DEFAULT_RESOLUTION = "1024x576"
    
    # Stability AI specific settings
    STABILITY_MODEL = "svd-xt-1-1"  # Stable Video Diffusion model
    STABILITY_BASE_URL = "https://api.stability.ai"
    
    # Available resolutions for Stability AI
    AVAILABLE_RESOLUTIONS = [
        "1024x576",   # 16:9 landscape
        "576x1024",   # 9:16 portrait  
        "768x768",    # Square
        "1024x1024"   # Large square
    ]
    
    # Available video styles
    STYLES = [
        "Realistic",
        "Cinematic", 
        "Animated",
        "Documentary",
        "Fantasy",
        "Sci-Fi"
    ]
    
    # File Settings
    TEMP_DIR = os.getenv("TEMP_DIR", "temp")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 100 * 1024 * 1024))  # 100MB default
    
    # API Settings
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", 300))  # 5 minutes default
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    
    @property
    def stability_api_key(self) -> str:
        """Get Stability AI API key"""
        return self.STABILITY_API_KEY
    
    @property
    def video_provider(self) -> VideoProvider:
        """Get the current video provider"""
        return self.DEFAULT_PROVIDER
    
    @staticmethod
    def get_api_key(provider: VideoProvider) -> str:
        """Get API key for specified provider"""
        if provider == VideoProvider.STABILITY_AI:
            return Config.STABILITY_API_KEY
        return ""
    
    @staticmethod
    def is_demo_mode() -> bool:
        """Check if running in demo mode (no API keys available)"""
        return not Config.STABILITY_API_KEY or not Config.validate_api_key()
    
    @staticmethod
    def validate_api_key() -> bool:
        """Validate if Stability AI API key is present and properly formatted"""
        api_key = Config.STABILITY_API_KEY
        return bool(
            api_key and 
            api_key.startswith('sk-') and 
            len(api_key) > 20
        )
    
    @staticmethod
    def get_provider_info() -> dict:
        """Get information about the current provider"""
        return {
            'name': 'Stability AI',
            'model': Config.STABILITY_MODEL,
            'max_duration': Config.MAX_DURATION,
            'min_duration': Config.MIN_DURATION,
            'resolutions': Config.AVAILABLE_RESOLUTIONS,
            'styles': Config.STYLES,
            'api_key_configured': Config.validate_api_key(),
            'demo_mode': Config.is_demo_mode()
        }
