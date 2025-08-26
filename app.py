import streamlit as st
import asyncio
import os
import time
import requests
import tempfile
from pathlib import Path

from video_generator import VideoGenerator
from config import Config

def add_futuristic_background():
    """Add sci-fi inspired dark theme styling"""
    st.markdown("""
    <style>
    /* Import futuristic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');
    
    /* Main space-like background gradient */
    .stApp {
        background: linear-gradient(135deg, #000428 0%, #004e92 25%, #001122 50%, #000000 100%);
        background-attachment: fixed;
        color: #00d9ff;
        font-family: 'Exo 2', sans-serif;
    }
    
    /* Animated starfield background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #ffffff, transparent),
            radial-gradient(2px 2px at 40px 70px, #00d9ff, transparent),
            radial-gradient(1px 1px at 190px 40px, #ffffff, transparent),
            radial-gradient(1px 1px at 130px 80px, #00d9ff, transparent),
            radial-gradient(2px 2px at 160px 30px, #ffffff, transparent),
            radial-gradient(1px 1px at 300px 120px, #00d9ff, transparent);
        background-repeat: repeat;
        background-size: 400px 300px;
        animation: stars 60s linear infinite;
        opacity: 0.3;
        z-index: -2;
        pointer-events: none;
    }
    
    @keyframes stars {
        from { transform: translateY(0px) translateX(0px); }
        to { transform: translateY(-400px) translateX(-200px); }
    }
    
    /* Floating particles animation */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(0, 217, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(0, 100, 200, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(0, 217, 255, 0.05) 0%, transparent 50%);
        animation: floating 20s ease-in-out infinite;
        z-index: -1;
        pointer-events: none;
    }
    
    @keyframes floating {
        0%, 100% { 
            transform: translate(0px, 0px) scale(1);
            opacity: 0.3;
        }
        33% { 
            transform: translate(30px, -30px) scale(1.1);
            opacity: 0.5;
        }
        66% { 
            transform: translate(-20px, 20px) scale(0.9);
            opacity: 0.4;
        }
    }
    
    /* Main content container - Glass morphism */
    .main .block-container {
        background: rgba(0, 30, 60, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 
            0 8px 32px rgba(0, 217, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 0 1px rgba(0, 217, 255, 0.05);
        position: relative;
        z-index: 10;
        margin: 1rem auto;
        max-width: none;
    }
    
    /* Sci-fi headers with neon glow */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', monospace !important;
        color: #00d9ff !important;
        text-shadow: 
            0 0 10px rgba(0, 217, 255, 0.8),
            0 0 20px rgba(0, 217, 255, 0.4),
            0 0 30px rgba(0, 217, 255, 0.2);
        text-align: center;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 1.8rem !important;
        margin: 1.5rem 0 1rem 0 !important;
    }
    
    h3 {
        font-size: 1.4rem !important;
        margin: 1rem 0 0.5rem 0 !important;
    }
    
    /* Futuristic buttons */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(0, 100, 200, 0.2) 100%);
        color: #00d9ff !important;
        border: 2px solid rgba(0, 217, 255, 0.3);
        border-radius: 50px;
        font-family: 'Orbitron', monospace;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 0.75rem 2rem;
        box-shadow: 
            0 0 20px rgba(0, 217, 255, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 217, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: #00d9ff;
        box-shadow: 
            0 5px 30px rgba(0, 217, 255, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2),
            0 0 40px rgba(0, 217, 255, 0.3);
        text-shadow: 0 0 10px rgba(0, 217, 255, 0.8);
    }
    
    .stButton > button:hover:before {
        left: 100%;
    }
    
    /* Sci-fi input fields */
    .stTextArea textarea, .stSelectbox select, .stTextInput input {
        background: rgba(0, 30, 60, 0.3) !important;
        border: 2px solid rgba(0, 217, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        font-family: 'Exo 2', sans-serif !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        backdrop-filter: blur(10px);
        box-shadow: 
            inset 0 2px 4px rgba(0, 0, 0, 0.3),
            0 0 15px rgba(0, 217, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus, .stSelectbox select:focus, .stTextInput input:focus {
        border-color: #00d9ff !important;
        box-shadow: 
            0 0 25px rgba(0, 217, 255, 0.5),
            inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        outline: none !important;
        background: rgba(0, 30, 60, 0.5) !important;
        color: #ffffff !important;
    }
    
    /* Placeholder styling */
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
        font-style: italic;
    }
    
    /* Labels and text */
    .stTextArea label, .stSelectbox label, .stTextInput label,
    .stSlider label, p, .stMarkdown, span, div {
        color: #00d9ff !important;
        font-family: 'Exo 2', sans-serif !important;
        font-weight: 400;
    }
    
    /* Selectbox dropdown styling */
    .stSelectbox > div > div {
        background: rgba(0, 30, 60, 0.9) !important;
        border: 1px solid rgba(0, 217, 255, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(15px);
        color: #ffffff !important;
    }
    
    .stSelectbox option {
        background: rgba(0, 30, 60, 0.9) !important;
        color: #ffffff !important;
    }
    
    /* Selectbox selected value */
    .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, rgba(0, 217, 255, 0.3), #00d9ff) !important;
        border-radius: 10px;
    }
    
    .stSlider > div > div > div > div > div {
        background: #00d9ff !important;
        border: 3px solid rgba(0, 30, 60, 0.8);
        box-shadow: 0 0 15px rgba(0, 217, 255, 0.6);
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #004e92, #00d9ff, #ffffff) !important;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 217, 255, 0.4);
    }
    
    /* Video container */
    .stVideo {
        border: 2px solid rgba(0, 217, 255, 0.4);
        border-radius: 20px;
        box-shadow: 
            0 0 30px rgba(0, 217, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        overflow: hidden;
    }
    
    /* Success and error messages */
    .stSuccess {
        background: rgba(0, 255, 150, 0.1) !important;
        border: 1px solid rgba(0, 255, 150, 0.3) !important;
        color: #00ff96 !important;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .stError {
        background: rgba(255, 50, 100, 0.1) !important;
        border: 1px solid rgba(255, 50, 100, 0.3) !important;
        color: #ff3264 !important;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    /* Spinner and loading states */
    .stSpinner > div {
        border-color: rgba(0, 217, 255, 0.3) rgba(0, 217, 255, 0.3) #00d9ff transparent !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(0, 30, 60, 0.3), rgba(0, 10, 30, 0.5)) !important;
        border-right: 2px solid rgba(0, 217, 255, 0.2);
        backdrop-filter: blur(15px);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 30, 60, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00d9ff, rgba(0, 217, 255, 0.3));
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 217, 255, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00d9ff;
        box-shadow: 0 0 15px rgba(0, 217, 255, 0.8);
    }
    
    /* Footer styling */
    .footer {
        background: rgba(0, 30, 60, 0.2);
        border-top: 1px solid rgba(0, 217, 255, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        text-align: center;
        backdrop-filter: blur(15px);
        box-shadow: 
            0 -5px 20px rgba(0, 217, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    .footer h3 {
        color: #00d9ff !important;
        font-family: 'Orbitron', monospace !important;
        text-shadow: 0 0 15px rgba(0, 217, 255, 0.6) !important;
    }
    
    .footer p {
        color: rgba(0, 217, 255, 0.8) !important;
        font-family: 'Exo 2', sans-serif !important;
    }
    
    /* Circular sci-fi indicators */
    .sci-fi-indicator {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: radial-gradient(circle, #00d9ff 30%, transparent 70%);
        box-shadow: 
            0 0 15px rgba(0, 217, 255, 0.6),
            inset 0 0 10px rgba(0, 217, 255, 0.3);
        animation: pulse 2s ease-in-out infinite;
        margin: 0 10px;
        display: inline-block;
    }
    
    @keyframes pulse {
        0%, 100% { 
            transform: scale(1);
            opacity: 0.8;
        }
        50% { 
            transform: scale(1.2);
            opacity: 1;
        }
    }
    
    /* Lock screen style placeholders */
    .lock-screen-element {
        position: relative;
        padding: 1rem;
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 50px;
        background: rgba(0, 30, 60, 0.1);
        backdrop-filter: blur(5px);
        margin: 0.5rem 0;
    }
    
    .lock-screen-element::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        border-radius: 50px;
        background: linear-gradient(45deg, #00d9ff, transparent, #00d9ff);
        animation: rotate 3s linear infinite;
        z-index: -1;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Ensure proper z-indexing */
    .stTextArea, .stSelectbox, .stTextInput, .stButton, .stSlider {
        position: relative;
        z-index: 100;
    }
    
    /* Fix any text visibility issues */
    .element-container {
        position: relative;
        z-index: 10;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Add futuristic background
    add_futuristic_background()
    
    st.title("Peppo AI Video Generator")
    st.markdown("### Generate AI Videos from Text Prompts with Stability AI")
    
    # Check API configuration
    config = Config()
    if config.is_demo_mode():
        st.warning("⚠️ Running in Demo Mode - Please add your Stability AI API key to generate real videos")
        st.info("💡 To use real video generation: Add your Stability AI API key to the .env file")
    
    st.markdown("---")
    
    # Initialize session state
    if 'video_generated' not in st.session_state:
        st.session_state.video_generated = False
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
    if 'video_url' not in st.session_state:
        st.session_state.video_url = None
    if 'image_path' not in st.session_state:
        st.session_state.image_path = None
    
    # User input section
    st.subheader("Enter Your Video Prompt")
    user_prompt = st.text_area(
        "Describe the video you want to generate:",
        placeholder="e.g., A cute cat playing with a ball of yarn in a sunny garden",
        height=100
    )
    
    # Video generation parameters
    st.subheader("Video Parameters")
    col1, col2 = st.columns(2)
    
    with col1:
        duration = st.slider("Duration (seconds)", 5, 10, 7)
        
    with col2:
        video_style = st.selectbox(
            "Video Style:",
            ["Realistic", "Cinematic", "Animated", "Documentary", "Fantasy", "Sci-Fi"]
        )
    
    st.markdown("---")
    
    # Generate button
    generate_col, _, download_col = st.columns([2, 1, 2])
    
    with generate_col:
        if st.button("Generate Video", type="primary", use_container_width=True):
            if not user_prompt.strip():
                st.error("Please enter a video prompt!")
            else:
                generate_video(user_prompt, duration, video_style)
    
    # Video display section
    if st.session_state.video_generated and (st.session_state.video_path or st.session_state.video_url or st.session_state.image_path):
        st.markdown("---")
        st.subheader("Generated Content")
        
        # Display video or image
        try:
            # Show image from Stability AI if available
            if hasattr(st.session_state, 'image_path') and st.session_state.image_path and os.path.exists(st.session_state.image_path):
                st.image(st.session_state.image_path, caption="Generated by Stability AI", use_container_width=True)
            
            # Show video (either real or demo)
            if hasattr(st.session_state, 'video_path') and st.session_state.video_path and os.path.exists(st.session_state.video_path):
                st.video(st.session_state.video_path)
            elif hasattr(st.session_state, 'video_url') and st.session_state.video_url:
                st.video(st.session_state.video_url)
        except Exception as e:
            st.error(f"Error displaying content: {str(e)}")
        
        # Download button
        with download_col:
            # Download image if available
            if hasattr(st.session_state, 'image_path') and st.session_state.image_path and os.path.exists(st.session_state.image_path):
                with open(st.session_state.image_path, "rb") as file:
                    st.download_button(
                        label="Download Image",
                        data=file.read(),
                        file_name=f"stability_image_{int(time.time())}.png",
                        mime="image/png",
                        type="secondary",
                        use_container_width=True
                    )
            # Download video if available
            elif hasattr(st.session_state, 'video_path') and st.session_state.video_path and os.path.exists(st.session_state.video_path):
                with open(st.session_state.video_path, "rb") as file:
                    st.download_button(
                        label="Download Video",
                        data=file.read(),
                        file_name=f"peppo_video_{int(time.time())}.mp4",
                        mime="video/mp4",
                        type="secondary",
                        use_container_width=True
                    )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div class='footer'>
            <h3>Peppo AI Engineering Internship Challenge</h3>
            <p>Powered by Stability AI - Generate amazing videos with AI!</p>
            <div style='margin-top: 1rem; display: flex; justify-content: center; align-items: center;'>
                <div class='sci-fi-indicator'></div>
                <div class='sci-fi-indicator'></div>
                <div class='sci-fi-indicator'></div>
                <div class='sci-fi-indicator'></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def generate_video(prompt, duration, style):
    """Generate video using Stability AI"""
    
    # Initialize video generator
    video_gen = VideoGenerator()
    config = Config()
    
    # Show configuration status
    if config.is_demo_mode():
        st.info("🔄 Running in Demo Mode - Simulating video generation")
    else:
        st.info("🚀 Using Stability AI for real video generation")
    
    with st.spinner(f"Generating video with Stability AI... This may take a few minutes."):
        try:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(percent, message):
                progress_bar.progress(percent)
                status_text.text(message)
            
            # Generate video using Stability AI
            result = asyncio.run(video_gen.generate_video(
                prompt=prompt,
                duration=duration,
                style=style,
                resolution="1024x576",
                progress_callback=update_progress
            ))
            
            if result['success']:
                # Handle different types of video data
                video_data = result['video_data']
                video_url = result.get('video_url')
                metadata = result.get('metadata', {})
                
                if video_data == b"demo_video_data" or not video_data:
                    # Demo mode - use the provided video URL
                    st.session_state.video_url = video_url
                    st.session_state.video_path = None
                    st.info("📺 Demo Mode: Showing sample video")
                    
                elif metadata.get('type') == 'image_from_api' and metadata.get('real_api'):
                    # Real image data from Stability AI
                    temp_dir = tempfile.gettempdir()
                    image_filename = f"stability_image_{int(time.time())}.png"
                    image_path = os.path.join(temp_dir, image_filename)
                    
                    with open(image_path, 'wb') as f:
                        f.write(video_data)
                    
                    st.session_state.video_path = None
                    st.session_state.image_path = image_path  # Store as image
                    # Also set a demo video to play alongside the image
                    st.session_state.video_url = video_url or "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
                    st.success("✅ Real image generated with Stability AI!")
                    st.info("🎨 Note: Stability AI generated a high-quality image (video generation not yet available)")
                    
                elif video_data and len(video_data) > 1000:
                    # Real video data - save to file
                    temp_dir = tempfile.gettempdir()
                    video_filename = f"stability_video_{int(time.time())}.mp4"
                    video_path = os.path.join(temp_dir, video_filename)
                    
                    with open(video_path, 'wb') as f:
                        f.write(video_data)
                    st.session_state.video_path = video_path
                    st.session_state.video_url = None
                    st.success("✅ Real video generated with Stability AI!")
                else:
                    # Fallback to URL if provided, or use demo video
                    st.session_state.video_url = video_url or "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
                    st.session_state.video_path = None
                    st.info("🔗 Video generated - streaming from URL")
                
                st.session_state.video_generated = True
                st.session_state.video_metadata = metadata
                
                progress_bar.empty()
                status_text.empty()
                
                # Show generation details
                metadata = result.get('metadata', {})
                if metadata:
                    with st.expander("📊 Generation Details"):
                        st.write(f"**Provider:** Stability AI")
                        st.write(f"**Model:** {metadata.get('model', 'svd-xt-1-1')}")
                        st.write(f"**Style:** {metadata.get('style', style)}")
                        st.write(f"**Duration:** {metadata.get('duration', duration)}s")
                        st.write(f"**Resolution:** {metadata.get('resolution', '1024x576')}")
                        if 'enhanced_prompt' in metadata:
                            st.write(f"**Enhanced Prompt:** {metadata['enhanced_prompt']}")
                        if metadata.get('demo_mode'):
                            st.write("**Mode:** Demo Mode (sample video)")
                
                st.rerun()
                
            else:
                error_msg = result.get('error', 'Unknown error occurred')
                st.error(f"❌ Video generation failed: {error_msg}")
                
                # Provide helpful error suggestions
                if "API key" in error_msg:
                    st.info("💡 Solution: Add your Stability AI API key to the .env file")
                elif "quota" in error_msg.lower() or "credit" in error_msg.lower():
                    st.info("💡 Solution: Check your Stability AI account credits and billing")
                elif "access" in error_msg.lower() or "permission" in error_msg.lower():
                    st.info("💡 Solution: Ensure your Stability AI account has video generation access")
                else:
                    st.info("💡 The app will continue in demo mode")
                
                # Set fallback demo video even when generation fails
                st.session_state.video_generated = True
                st.session_state.video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
                st.session_state.video_path = None
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.info("🔄 Falling back to demo mode...")
            
            # Fallback to demo mode
            st.session_state.video_generated = True
            st.session_state.video_url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
            st.session_state.video_path = None
            st.rerun()

def create_demo_video(prompt, duration, style):
    """Create a demo video file (placeholder for actual Sora integration)"""
    # This function is kept for backward compatibility but is now handled by StabilityAIClient
    temp_dir = tempfile.gettempdir()
    video_filename = f"stability_demo_{int(time.time())}.mp4"
    video_path = os.path.join(temp_dir, video_filename)
    return video_path

if __name__ == "__main__":
    main()
