"""
Test script to verify Stability AI API connection
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_stability_api():
    """Test Stability AI API connection and key validity"""
    
    api_key = os.getenv("STABILITY_API_KEY", "")
    
    print("🔍 Testing Stability AI API...")
    print(f"API Key: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else 'invalid'}")
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    if not api_key.startswith('sk-'):
        print("❌ Invalid API key format (should start with 'sk-')")
        return False
    
    # Test API connection
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test with account endpoint
        print("📡 Testing API connection...")
        response = requests.get(
            "https://api.stability.ai/v1/user/account",
            headers=headers,
            timeout=10
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            account_data = response.json()
            print("✅ API connection successful!")
            print(f"Account ID: {account_data.get('id', 'Unknown')}")
            print(f"Credits: {account_data.get('credits', 'Unknown')}")
            return True
        
        elif response.status_code == 401:
            print("❌ Unauthorized - Invalid API key")
            print("💡 Please check your API key at https://platform.stability.ai/")
            return False
        
        elif response.status_code == 429:
            print("⚠️  Rate limited - Too many requests")
            return False
        
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print("❌ Request timeout - API is slow to respond")
        return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Check your internet connection")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_image_generation():
    """Test basic image generation to verify API works"""
    
    api_key = os.getenv("STABILITY_API_KEY", "")
    
    if not api_key:
        print("❌ No API key for image generation test")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Simple text-to-image request with correct SDXL dimensions
    payload = {
        "text_prompts": [
            {
                "text": "a beautiful sunset over mountains",
                "weight": 1.0
            }
        ],
        "cfg_scale": 7,
        "height": 1024,  # SDXL requires specific dimensions
        "width": 1024,   # 1024x1024 is allowed
        "samples": 1,
        "steps": 20
    }
    
    try:
        print("🎨 Testing image generation...")
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"Image generation status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'artifacts' in result and len(result['artifacts']) > 0:
                print("✅ Image generation successful!")
                print(f"Generated {len(result['artifacts'])} image(s)")
                return True
            else:
                print("❌ No images generated")
                return False
        
        elif response.status_code == 401:
            print("❌ Unauthorized for image generation")
            return False
        
        elif response.status_code == 402:
            print("❌ Insufficient credits")
            return False
        
        elif response.status_code == 429:
            print("⚠️  Rate limited")
            return False
        
        else:
            print(f"❌ Image generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Image generation error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Stability AI API Test")
    print("=" * 50)
    
    # Test 1: API Connection
    connection_ok = test_stability_api()
    print()
    
    # Test 2: Image Generation
    if connection_ok:
        image_ok = test_image_generation()
        print()
        
        if image_ok:
            print("🎉 All tests passed! Your API key is working correctly.")
            print("💡 The app should now be able to generate real videos!")
        else:
            print("⚠️  API connection works but image generation failed.")
            print("💡 The app will fall back to demo mode.")
    else:
        print("❌ API connection failed. App will run in demo mode only.")
    
    print("\n" + "=" * 50)
