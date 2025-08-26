"""
File handling utilities for video generation and management.
"""

import os
import tempfile
import uuid
from datetime import datetime
from typing import Optional
import cv2
import numpy as np
from config import VideoProvider


class FileHandler:
    """Handles file operations for video generation and storage."""
    
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        self.output_dir = os.path.join(os.getcwd(), "generated_videos")
        self.ensure_output_directory()
    
    def ensure_output_directory(self):
        """Ensure the output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def save_video(self, video_data: bytes, prompt: str, provider: VideoProvider) -> Optional[str]:
        """
        Save video data to a file.
        
        Args:
            video_data: Raw video data as bytes
            prompt: Original prompt used for generation
            provider: Video provider used
            
        Returns:
            Path to saved video file or None if failed
        """
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:30] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_prompt = safe_prompt.replace(' ', '_')
            
            filename = f"{timestamp}_{provider.value}_{safe_prompt}.mp4"
            filepath = os.path.join(self.output_dir, filename)
            
            # Save video data
            with open(filepath, 'wb') as f:
                f.write(video_data)
            
            # Verify file was saved successfully
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                return filepath
            else:
                print(f"Failed to save video file: {filepath}")
                return None
                
        except Exception as e:
            print(f"Error saving video: {str(e)}")
            return None
    
    def create_temp_file(self, suffix: str = ".mp4") -> str:
        """Create a temporary file and return its path."""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        temp_file.close()
        return temp_file.name
    
    def create_demo_video(self, prompt: str, duration: int, style: str, provider: VideoProvider) -> str:
        """
        Create a demo video for demonstration purposes.
        
        Args:
            prompt: Text prompt for the video
            duration: Duration in seconds
            style: Video style
            provider: Provider used
            
        Returns:
            Path to created demo video
        """
        try:
            # Create a simple demo video with text overlay
            width, height = 1280, 720
            fps = 24
            total_frames = duration * fps
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"demo_{timestamp}_{provider.value}.mp4"
            filepath = os.path.join(self.output_dir, filename)
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
            
            # Generate frames
            for frame_num in range(total_frames):
                # Create a gradient background
                frame = self._create_gradient_frame(width, height, frame_num, total_frames, style)
                
                # Add text overlay
                self._add_text_overlay(frame, prompt, provider, frame_num, total_frames)
                
                out.write(frame)
            
            out.release()
            cv2.destroyAllWindows()
            
            return filepath
            
        except Exception as e:
            print(f"Error creating demo video: {str(e)}")
            # Return a placeholder path
            return self.create_temp_file()
    
    def _create_gradient_frame(self, width: int, height: int, frame_num: int, total_frames: int, style: str) -> np.ndarray:
        """Create a gradient background frame."""
        # Create base gradient
        gradient = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Style-based color schemes
        color_schemes = {
            "Cinematic": [(20, 30, 60), (80, 120, 200)],
            "Realistic": [(40, 60, 40), (120, 150, 120)],
            "Artistic": [(60, 20, 80), (200, 100, 180)],
            "Fantasy": [(40, 20, 60), (160, 100, 200)],
            "Sci-Fi": [(10, 30, 50), (50, 150, 255)],
            "Animation": [(80, 40, 20), (255, 200, 100)],
            "Abstract": [(30, 50, 30), (150, 200, 150)],
            "Documentary": [(50, 50, 50), (150, 150, 150)]
        }
        
        colors = color_schemes.get(style, [(30, 30, 30), (100, 100, 100)])
        
        # Animate colors based on frame
        progress = frame_num / total_frames
        color1 = np.array(colors[0])
        color2 = np.array(colors[1])
        
        # Create animated gradient
        for y in range(height):
            blend = (y / height + progress * 0.5) % 1.0
            color = color1 * (1 - blend) + color2 * blend
            gradient[y, :] = color.astype(np.uint8)
        
        return gradient
    
    def _add_text_overlay(self, frame: np.ndarray, prompt: str, provider: VideoProvider, frame_num: int, total_frames: int):
        """Add text overlay to frame."""
        height, width = frame.shape[:2]
        
        # Add provider watermark
        cv2.putText(frame, f"Generated with {provider.value}", 
                   (20, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add prompt (truncated)
        prompt_text = prompt[:50] + "..." if len(prompt) > 50 else prompt
        cv2.putText(frame, f"Prompt: {prompt_text}", 
                   (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Add demo watermark
        cv2.putText(frame, "DEMO VIDEO", 
                   (width // 2 - 100, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        
        # Add frame counter
        cv2.putText(frame, f"Frame {frame_num + 1}/{total_frames}", 
                   (width - 200, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    def get_video_info(self, video_path: str) -> dict:
        """Get information about a video file."""
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return {}
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            return {
                "duration": duration,
                "fps": fps,
                "width": width,
                "height": height,
                "frame_count": frame_count,
                "file_size": os.path.getsize(video_path)
            }
            
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return {}
    
    def cleanup(self):
        """Clean up temporary files."""
        try:
            # Clean up old temporary files
            temp_files = [f for f in os.listdir(self.temp_dir) if f.startswith('tmp') and f.endswith('.mp4')]
            for temp_file in temp_files:
                try:
                    os.remove(os.path.join(self.temp_dir, temp_file))
                except:
                    pass
        except Exception as e:
            print(f"Cleanup error: {str(e)}")
    
    def list_generated_videos(self) -> list:
        """List all generated videos."""
        try:
            if not os.path.exists(self.output_dir):
                return []
            
            videos = []
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.mp4'):
                    filepath = os.path.join(self.output_dir, filename)
                    stat = os.stat(filepath)
                    videos.append({
                        "filename": filename,
                        "filepath": filepath,
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(stat.st_ctime),
                        "modified": datetime.fromtimestamp(stat.st_mtime)
                    })
            
            # Sort by creation time, newest first
            videos.sort(key=lambda x: x["created"], reverse=True)
            return videos
            
        except Exception as e:
            print(f"Error listing videos: {str(e)}")
            return []
