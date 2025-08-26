"""
Video generation orchestrator using Stability AI
"""

import asyncio
import tempfile
import time
import streamlit as st
from typing import Optional, Dict, Any, Callable
from pathlib import Path

from config import Config, VideoProvider
from api_clients.stability_ai_client import StabilityAIClient


class VideoGenerator:
    """Stability AI video generation orchestrator"""
    
    def __init__(self):
        self.config = Config()
        self._client = None
        
    async def initialize(self):
        """Initialize the Stability AI client"""
        try:
            if not self.config.stability_api_key:
                print("⚠️  No Stability AI API key found, using demo mode")
                
            self._client = StabilityAIClient(self.config.stability_api_key)
                
        except Exception as e:
            print(f"⚠️  Failed to initialize Stability AI client: {e}")
            print("🔄 Will use demo mode")
    
    async def generate_video(
        self,
        prompt: str,
        duration: int = 7,
        style: str = "Realistic",
        resolution: str = "1024x576",
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Generate video using Stability AI
        
        Args:
            prompt: Text description for video generation
            duration: Video duration in seconds (5-10)
            style: Video style preference
            resolution: Video resolution
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dict containing video data and metadata
        """
        if not self._client:
            await self.initialize()
        
        try:
            # Validate input parameters
            self._validate_inputs(prompt, duration, style, resolution)
            
            if progress_callback:
                progress_callback(5, "Starting Stability AI video generation...")
            
            # Generate video using Stability AI client
            result = await self._client.generate_video(
                prompt=prompt,
                duration=duration,
                style=style,
                resolution=resolution,
                progress_callback=progress_callback
            )
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Stability AI video generation failed: {str(e)}",
                'video_data': None
            }
    
    def _validate_inputs(self, prompt: str, duration: int, style: str, resolution: str):
        """Validate input parameters for Stability AI"""
        
        if not prompt or len(prompt.strip()) < 10:
            raise ValueError("Prompt must be at least 10 characters long")
        
        if duration < 5 or duration > 10:
            raise ValueError("Duration must be between 5 and 10 seconds")
        
        valid_styles = ["Realistic", "Cinematic", "Animated", "Documentary", "Fantasy", "Sci-Fi"]
        if style not in valid_styles:
            raise ValueError(f"Style must be one of: {', '.join(valid_styles)}")
        
        valid_resolutions = ["1024x576", "576x1024", "768x768", "1024x1024"]
        if resolution not in valid_resolutions:
            raise ValueError(f"Resolution must be one of: {', '.join(valid_resolutions)}")
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the Stability AI provider"""
        return {
            'provider': 'Stability AI',
            'model': 'svd-xt-1-1',
            'available': self._client is not None,
            'capabilities': {
                'max_duration': 10,
                'min_duration': 5,
                'supported_resolutions': ["1024x576", "576x1024", "768x768", "1024x1024"],
                'supported_styles': ["Realistic", "Cinematic", "Animated", "Documentary", "Fantasy", "Sci-Fi"]
            }
        }
    
    async def get_generation_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get status of a video generation job
        
        Args:
            job_id: The generation job ID
            
        Returns:
            Status information
        """
        if not self._client:
            await self.initialize()
            
        return await self._client.get_generation_status(job_id)
    
    def cleanup(self):
        """Clean up temporary files and resources."""
        try:
            # Clean up any temporary files if needed
            pass
        except Exception as e:
            st.warning(f"Cleanup warning: {str(e)}")
