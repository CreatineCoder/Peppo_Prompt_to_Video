#!/usr/bin/env python3
"""
Setup script for Peppo AI Video Generator
This script helps set up the environment and dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🎬 Peppo AI Video Generator - Setup Script")
    print("=" * 60)
    print()


def check_python_version():
    """Check if Python version is compatible"""
    print("📋 Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor} - Compatible")
    return True


def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_environment():
    """Set up environment file"""
    print("\n🔧 Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("⚠️  .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ .env.example file not found")
        return False
    
    # Copy example to .env
    shutil.copy(env_example, env_file)
    print("✅ Created .env file from template")
    
    return True


def check_api_key():
    """Check if API key is configured"""
    print("\n🔑 Checking API configuration...")
    
    api_key = os.getenv("OPENAI_API_KEY", "")
    
    if not api_key or api_key.startswith("sk-your-"):
        print("⚠️  OpenAI API key not configured")
        print("   Please edit .env file and add your OpenAI API key")
        print("   Get your key from: https://platform.openai.com/api-keys")
        print("   Note: Sora access requires special approval from OpenAI")
        return False
    
    if not api_key.startswith("sk-"):
        print("❌ Invalid API key format")
        return False
    
    print("✅ API key configured")
    return True


def create_temp_directory():
    """Create temporary directory for videos"""
    print("\n📁 Setting up directories...")
    
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    print("✅ Temp directory created")
    return True


def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    required_modules = [
        "streamlit",
        "openai", 
        "requests",
        "PIL",
        "cv2",
        "numpy"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("✅ All imports successful")
    return True


def show_next_steps():
    """Show next steps to user"""
    print("\n" + "=" * 60)
    print("🚀 Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run the application:")
    print("   streamlit run app.py")
    print()
    print("3. Open your browser to: http://localhost:8501")
    print()
    print("📚 For help:")
    print("   - Check README.md for detailed instructions")
    print("   - Visit: https://platform.openai.com/docs")
    print()
    print("🎬 Ready to generate amazing videos with AI!")
    print()


def main():
    """Main setup function"""
    print_banner()
    
    # Check requirements
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Set up environment
    if not setup_environment():
        print("\n❌ Setup failed at environment configuration")
        sys.exit(1)
    
    # Create directories
    if not create_temp_directory():
        print("\n❌ Setup failed at directory creation")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("\n❌ Setup failed at import testing")
        print("Try running: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check API key (warning only)
    check_api_key()
    
    # Show next steps
    show_next_steps()


if __name__ == "__main__":
    main()
