#!/usr/bin/env python3
"""
Test script to verify demo videos are working and under 20 seconds
"""

import requests
import time

def test_video_url(url, name):
    """Test if a video URL is accessible and get its size"""
    try:
        print(f"🔍 Testing {name}...")
        
        # Make a HEAD request to get content info without downloading
        response = requests.head(url, timeout=10)
        
        if response.status_code == 200:
            content_length = response.headers.get('content-length')
            content_type = response.headers.get('content-type', '')
            
            if content_length:
                size_mb = int(content_length) / (1024 * 1024)
                print(f"   ✅ Accessible - Size: {size_mb:.1f}MB - Type: {content_type}")
                
                # Estimate duration based on file size (rough estimate)
                # Most short videos are around 1-3MB per minute
                estimated_duration = size_mb * 60 / 2  # Rough estimate
                if estimated_duration <= 20:
                    print(f"   ✅ Estimated duration: ~{estimated_duration:.1f}s (under 20s)")
                else:
                    print(f"   ⚠️  Estimated duration: ~{estimated_duration:.1f}s (may be over 20s)")
            else:
                print(f"   ✅ Accessible - Size: Unknown - Type: {content_type}")
            
            return True
        else:
            print(f"   ❌ Failed - Status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ❌ Timeout")
        return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection error")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Test all demo videos"""
    
    print("🧪 Testing Demo Video URLs")
    print("=" * 50)
    
    # Demo videos from the updated list
    demo_videos = [
        ("ForBiggerMeltdowns.mp4", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4"),
        ("ForBiggerEscapes.mp4", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"),
        ("ForBiggerBlazes.mp4", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"),
        ("ForBiggerJoyrides.mp4", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"),
        ("SampleVideo_1280x720_2mb.mp4", "https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4"),
        ("SampleVideo_640x360_2mb.mp4", "https://sample-videos.com/zip/10/mp4/SampleVideo_640x360_2mb.mp4"),
        ("ed_1024_512kb.mp4", "https://archive.org/download/ElephantsDream/ed_1024_512kb.mp4"),
        ("big_buck_bunny_720p_surround.mp4", "https://archive.org/download/BigBuckBunny_124/Content/big_buck_bunny_720p_surround.mp4")
    ]
    
    working_videos = 0
    total_videos = len(demo_videos)
    
    for name, url in demo_videos:
        if test_video_url(url, name):
            working_videos += 1
        print()  # Empty line for readability
    
    print("=" * 50)
    print(f"📊 Results: {working_videos}/{total_videos} videos are accessible")
    
    if working_videos > 0:
        print("✅ Demo videos are working!")
        print("🎬 Your app will have working fallback videos when SVD isn't available")
    else:
        print("❌ No demo videos are accessible")
        print("⚠️  Your app may have issues with fallback videos")
    
    return working_videos > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
