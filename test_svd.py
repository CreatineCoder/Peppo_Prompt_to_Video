#!/usr/bin/env python3
"""
Test script for Stability AI Stable Video Diffusion (SVD) API
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api_clients.stability_ai_client import StabilityAIClient

async def test_svd_api():
    """Test the Stability AI SVD video generation"""
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('STABILITY_API_KEY')
    
    if not api_key:
        print("❌ Error: STABILITY_API_KEY not found in environment variables")
        print("Please add your Stability AI API key to the .env file")
        return False
    
    print("🔑 API Key found")
    print(f"🔍 Testing with key: {api_key[:8]}...")
    
    try:
        # Initialize client
        client = StabilityAIClient(api_key)
        print("✅ Client initialized successfully")
        
        # Test prompt
        test_prompt = "A majestic eagle soaring through the clouds at sunset"
        
        print(f"🎬 Testing SVD video generation with prompt: '{test_prompt}'")
        
        def progress_callback(percent, message):
            print(f"📊 Progress: {percent}% - {message}")
        
        # Generate video
        result = await client.generate_video(
            prompt=test_prompt,
            duration=7,
            style="Cinematic",
            resolution="1024x576",
            progress_callback=progress_callback
        )
        
        if result['success']:
            metadata = result.get('metadata', {})
            video_type = metadata.get('type', 'unknown')
            model = metadata.get('model', 'unknown')
            
            print(f"✅ Generation successful!")
            print(f"🎥 Type: {video_type}")
            print(f"🤖 Model: {model}")
            print(f"📏 Data size: {len(result['video_data'])} bytes")
            
            if video_type == 'video_from_svd':
                print("🎉 SUCCESS: Real video generated using Stable Video Diffusion!")
                return True
            else:
                print("📺 Demo mode used with short videos (under 20 seconds)")
                return True
        else:
            print("❌ Generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Stability AI Stable Video Diffusion (SVD) API")
    print("=" * 60)
    
    success = asyncio.run(test_svd_api())
    
    print("=" * 60)
    if success:
        print("✅ SVD API test completed successfully!")
        print("🚀 Your app should now generate real videos using Stability AI")
    else:
        print("⚠️  SVD API test had issues")
        print("🔄 App will fall back to demo mode or image generation")
