"""
Pika Labs API client for video generation.
"""

import requests
import asyncio
import time
from typing import Optional, Dict, Any


class PikaClient:
    """Client for interacting with Pika Labs API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.pika.art/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_video(self, prompt: str, duration: int, style: str) -> Optional[bytes]:
        """
        Generate video using Pika Labs API.
        
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
                "duration": min(duration, 6),  # Pika max is 6 seconds
                "aspect_ratio": "16:9",
                "frame_rate": 24,
                "style": self._map_style_to_pika(style),
                "motion": "medium",
                "guidance_scale": 7.5
            }
            
            # Start video generation
            response = requests.post(
                f"{self.base_url}/videos/generate",
                headers=self.headers,
                json=generation_data,
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"Pika generation failed: {response.status_code} - {response.text}")
                return None
            
            generation_id = response.json().get("id")
            if not generation_id:
                print("No generation ID received from Pika")
                return None
            
            # Poll for completion
            video_data = await self._poll_generation_status(generation_id)
            return video_data
            
        except Exception as e:
            print(f"Pika client error: {str(e)}")
            return None
    
    def _map_style_to_pika(self, style: str) -> str:
        """Map general style to Pika Labs style."""
        style_mapping = {
            "Cinematic": "cinematic",
            "Realistic": "realistic",
            "Artistic": "artistic",
            "Fantasy": "fantasy",
            "Sci-Fi": "futuristic",
            "Animation": "cartoon",
            "Abstract": "abstract",
            "Documentary": "realistic"
        }
        return style_mapping.get(style, "realistic")
    
    async def _poll_generation_status(self, generation_id: str) -> Optional[bytes]:
        """Poll the generation status until completion."""
        max_attempts = 60  # 5 minutes with 5-second intervals
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = requests.get(
                    f"{self.base_url}/videos/{generation_id}",
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status")
                    
                    if status == "completed":
                        # Download the video
                        video_url = data.get("video_url")
                        if video_url:
                            return await self._download_video(video_url)
                        else:
                            print("No video URL in response")
                            return None
                    elif status == "failed":
                        print(f"Pika generation failed: {data.get('error', 'Unknown error')}")
                        return None
                    elif status in ["pending", "processing", "queued"]:
                        # Continue polling
                        await asyncio.sleep(5)
                        attempt += 1
                    else:
                        print(f"Unknown status from Pika: {status}")
                        return None
                else:
                    print(f"Status check failed: {response.status_code}")
                    return None
                    
            except Exception as e:
                print(f"Error checking status: {str(e)}")
                await asyncio.sleep(5)
                attempt += 1
        
        print("Pika generation timed out")
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
                f"{self.base_url}/user/profile",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
