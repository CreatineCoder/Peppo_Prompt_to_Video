import os
from enum import Enum

class VideoProvider(Enum):
    RUNWAY = "runway"
    STABLE_VIDEO = "stable_video"
    PIKA = "pika"

class Config:
    # API Configuration
    DEFAULT_PROVIDER = VideoProvider.RUNWAY
    
    # API Keys (loaded from environment variables)
    RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY", "")
    STABLE_VIDEO_API_KEY = os.getenv("STABLE_VIDEO_API_KEY", "")
    PIKA_API_KEY = os.getenv("PIKA_API_KEY", "")
    
    # Video Generation Settings
    DEFAULT_DURATION = 7
    MIN_DURATION = 5
    MAX_DURATION = 10
    
    # File Settings
    TEMP_DIR = os.getenv("TEMP_DIR", "temp")
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    
    # UI Settings
    STYLES = ["Realistic", "Animated", "Cinematic", "Abstract"]
    
    @staticmethod
    def get_api_key(provider: VideoProvider) -> str:
        """Get API key for specified provider"""
        if provider == VideoProvider.RUNWAY:
            return Config.RUNWAY_API_KEY
        elif provider == VideoProvider.STABLE_VIDEO:
            return Config.STABLE_VIDEO_API_KEY
        elif provider == VideoProvider.PIKA:
            return Config.PIKA_API_KEY
        return ""
    
    @staticmethod
    def is_demo_mode() -> bool:
        """Check if running in demo mode (no API keys)"""
        return not any([
            Config.RUNWAY_API_KEY,
            Config.STABLE_VIDEO_API_KEY,
            Config.PIKA_API_KEY
        ])
