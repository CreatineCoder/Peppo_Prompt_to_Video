"""
Stable Video Diffusion API client for video generation.
"""

import requests
import asyncio
import time
from typing import Optional, Dict, Any


class StableVideoClient:
    """Client for interacting with Stable Video Diffusion API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v2alpha"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def generate_video(self, prompt: str, duration: int, style: str) -> Optional[bytes]:
        """
        Generate video using Stable Video Diffusion API.
        
        Args:
            prompt: Text description for video generation
            duration: Video duration in seconds
            style: Visual style for the video
            
        Returns:
            Video data as bytes or None if failed
        """
        try:
            # Prepare generation request
            generation_data = {
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "duration": duration,
                "cfg_scale": 7.5,
                "motion_bucket_id": 127,
                "seed": None,  # Random seed
                "style_preset": self._map_style_to_preset(style)
            }
            
            # Start video generation
            response = requests.post(
                f"{self.base_url}/generation/video",
                headers=self.headers,
                json=generation_data,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Stable Video generation failed: {response.status_code} - {response.text}")
                return None
            
            generation_id = response.json().get("id")
            if not generation_id:
                print("No generation ID received from Stable Video")
                return None
            
            # Poll for completion
            video_data = await self._poll_generation_status(generation_id)
            return video_data
            
        except Exception as e:
            print(f"Stable Video client error: {str(e)}")
            return None
    
    def _map_style_to_preset(self, style: str) -> str:
        """Map general style to Stable Video style preset."""
        style_mapping = {
            "Cinematic": "cinematic",
            "Realistic": "photographic",
            "Artistic": "artistic",
            "Fantasy": "fantasy-art",
            "Sci-Fi": "digital-art",
            "Animation": "anime",
            "Abstract": "artistic",
            "Documentary": "photographic"
        }
        return style_mapping.get(style, "photographic")
    
    async def _poll_generation_status(self, generation_id: str) -> Optional[bytes]:
        """Poll the generation status until completion."""
        max_attempts = 60  # 5 minutes with 5-second intervals
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get(
                    f"{self.base_url}/generation/video/{generation_id}",
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")
                    
                    if status == "complete":
                        # Download the video
                        video_url = data.get("artifacts", [{}])[0].get("url")
                        if video_url:
                            return await self._download_video(video_url)
                        else:
                            print("No video URL in response")
                            return None
                    elif status == "failed":
                        print(f"Stable Video generation failed: {data.get('failure_reason', 'Unknown error')}")
                        return None
                    elif status in ["in-progress", "queued"]:
                        # Continue polling
                        await asyncio.sleep(5)
                        attempt += 1
                    else:
                        print(f"Unknown status from Stable Video: {status}")
                        return None
                else:
                    print(f"Status check failed: {response.status_code}")
                    return None
                    
            except Exception as e:
                print(f"Error checking status: {str(e)}")
                await asyncio.sleep(5)
                attempt += 1
        
        print("Stable Video generation timed out")
        return None
    
    async def _download_video(self, video_url: str) -> Optional[bytes]:
        """Download video from the provided URL."""
        try:
            response = requests.get(video_url, timeout=60)
            if response.status_code == 200:
                return response.content
            else:
                print(f"Video download failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """Test if the API connection is working."""
        try:
            response = requests.get(
                f"{self.base_url}/user/account",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
