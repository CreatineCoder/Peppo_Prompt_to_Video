"""
Video generation orchestrator that handles different AI video providers.
"""

import streamlit as st
import time
import random
from typing import Optional, Dict, Any
from config import Config, VideoProvider
from api_clients.runway_client import RunwayClient
from api_clients.stable_video_client import StableVideoClient
from api_clients.pika_client import PikaClient
from utils.file_handler import FileHandler


class VideoGenerator:
    """Main video generation controller that manages different AI providers."""
    
    def __init__(self):
        self.config = Config()
        self.file_handler = FileHandler()
        self.clients = {}
        self._init_clients()
    
    def _init_clients(self):
        """Initialize available API clients based on configuration."""
        try:
            # Initialize Runway client if API key is available
            if self.config.get_api_key(VideoProvider.RUNWAY):
                self.clients[VideoProvider.RUNWAY] = RunwayClient(
                    self.config.get_api_key(VideoProvider.RUNWAY)
                )
            
            # Initialize Stable Video client if API key is available
            if self.config.get_api_key(VideoProvider.STABLE_VIDEO):
                self.clients[VideoProvider.STABLE_VIDEO] = StableVideoClient(
                    self.config.get_api_key(VideoProvider.STABLE_VIDEO)
                )
            
            # Initialize Pika Labs client if API key is available
            if self.config.get_api_key(VideoProvider.PIKA):
                self.clients[VideoProvider.PIKA] = PikaClient(
                    self.config.get_api_key(VideoProvider.PIKA)
                )
                
        except Exception as e:
            st.error(f"Error initializing API clients: {str(e)}")
    
    def get_available_providers(self) -> list[VideoProvider]:
        """Get list of available video providers based on API keys."""
        if self.config.is_demo_mode():
            return [VideoProvider.RUNWAY, VideoProvider.STABLE_VIDEO, VideoProvider.PIKA]
        return list(self.clients.keys())
    
    def _validate_inputs(self, prompt: str, duration: int, style: str) -> bool:
        """Validate user inputs before generation."""
        if not prompt or len(prompt.strip()) < 10:
            st.error("Please provide a detailed prompt (at least 10 characters)")
            return False
        
        if not (self.config.MIN_DURATION <= duration <= self.config.MAX_DURATION):
            st.error(f"Duration must be between {self.config.MIN_DURATION} and {self.config.MAX_DURATION} seconds")
            return False
        
        if style not in self.config.STYLES:
            st.error("Please select a valid style")
            return False
        
        return True
    
    def _generate_demo_video(self, prompt: str, duration: int, style: str, provider: VideoProvider) -> Optional[str]:
        """Generate a demo video for demonstration purposes."""
        # Simulate video generation process
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        stages = [
            "Analyzing prompt...",
            "Preparing AI model...",
            f"Generating {duration}s video with {provider.value}...",
            "Processing frames...",
            "Optimizing output...",
            "Finalizing video..."
        ]
        
        for i, stage in enumerate(stages):
            status_text.text(stage)
            progress_bar.progress((i + 1) / len(stages))
            time.sleep(random.uniform(0.5, 1.5))  # Simulate processing time
        
        status_text.text("Video generation complete!")
        
        # Create a demo video file (placeholder)
        demo_video_path = self.file_handler.create_demo_video(prompt, duration, style, provider)
        return demo_video_path
    
    async def generate_video(self, prompt: str, duration: int, style: str, provider: VideoProvider) -> Optional[str]:
        """
        Generate a video using the specified provider.
        
        Args:
            prompt: Text description for video generation
            duration: Video duration in seconds
            style: Visual style for the video
            provider: AI provider to use for generation
            
        Returns:
            Path to generated video file or None if failed
        """
        # Validate inputs
        if not self._validate_inputs(prompt, duration, style):
            return None
        
        # Check if in demo mode
        if self.config.is_demo_mode():
            st.info("Running in demo mode - generating placeholder video")
            return self._generate_demo_video(prompt, duration, style, provider)
        
        # Check if provider is available
        if provider not in self.clients:
            st.error(f"{provider.value} is not available. Please check API configuration.")
            return None
        
        try:
            client = self.clients[provider]
            
            # Show generation progress
            with st.spinner(f"Generating video with {provider.value}..."):
                # Generate video using the specific client
                video_data = await client.generate_video(
                    prompt=prompt,
                    duration=duration,
                    style=style
                )
                
                if video_data:
                    # Save the generated video
                    video_path = self.file_handler.save_video(
                        video_data=video_data,
                        prompt=prompt,
                        provider=provider
                    )
                    
                    if video_path:
                        st.success(f"Video generated successfully with {provider.value}!")
                        return video_path
                    else:
                        st.error("Failed to save generated video")
                        return None
                else:
                    st.error(f"Failed to generate video with {provider.value}")
                    return None
                    
        except Exception as e:
            st.error(f"Error during video generation: {str(e)}")
            return None
    
    def get_provider_info(self, provider: VideoProvider) -> Dict[str, Any]:
        """Get information about a specific provider."""
        provider_info = {
            VideoProvider.RUNWAY: {
                "name": "Runway ML",
                "description": "High-quality cinematic video generation",
                "max_duration": 10,
                "specialties": ["Cinematic", "Realistic", "Motion"]
            },
            VideoProvider.STABLE_VIDEO: {
                "name": "Stable Video Diffusion",
                "description": "Stable and consistent video generation",
                "max_duration": 8,
                "specialties": ["Consistent", "Stable", "Detailed"]
            },
            VideoProvider.PIKA: {
                "name": "Pika Labs",
                "description": "Creative and artistic video generation",
                "max_duration": 6,
                "specialties": ["Creative", "Artistic", "Stylized"]
            }
        }
        
        return provider_info.get(provider, {})
    
    def cleanup(self):
        """Clean up temporary files and resources."""
        try:
            self.file_handler.cleanup()
        except Exception as e:
            st.warning(f"Cleanup warning: {str(e)}")
