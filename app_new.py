"""
Peppo AI Video Generation Platform
A futuristic interface for generating AI videos using multiple providers.
"""

import streamlit as st
import asyncio
from datetime import datetime
from config import Config, VideoProvider
from video_generator import VideoGenerator


def add_futuristic_background():
    """Add futuristic CSS styling with animated background"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600&display=swap');
    
    /* Main app container */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Animated gradient background */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Particle effect overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #00d9ff, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.3), transparent),
            radial-gradient(1px 1px at 90px 40px, #00d9ff, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.2), transparent),
            radial-gradient(2px 2px at 160px 30px, #00d9ff, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: sparkle 20s linear infinite;
        pointer-events: none;
        z-index: 1;
    }
    
    @keyframes sparkle {
        from { transform: translateY(0px); }
        to { transform: translateY(-100px); }
    }
    
    /* Grid overlay */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(0, 217, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 217, 255, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridPulse 8s ease-in-out infinite;
        pointer-events: none;
        z-index: 2;
    }
    
    @keyframes gridPulse {
        0%, 100% { opacity: 0.1; }
        50% { opacity: 0.3; }
    }
    
    /* Main content styling */
    .main > div {
        position: relative;
        z-index: 10;
        background: rgba(10, 15, 35, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(0, 217, 255, 0.2);
        padding: 2rem;
        margin: 1rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }
    
    /* Typography */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Orbitron', monospace !important;
        color: #00d9ff !important;
        text-shadow: 0 0 10px rgba(0, 217, 255, 0.5);
        text-align: center;
    }
    
    h1, .stMarkdown h1 {
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        margin-bottom: 2rem !important;
        background: linear-gradient(45deg, #00d9ff, #ffffff, #00d9ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: textGlow 3s ease-in-out infinite;
    }
    
    @keyframes textGlow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    p, .stMarkdown p, .stText, label {
        font-family: 'Exo 2', sans-serif !important;
        color: #e0e6ed !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(15, 25, 50, 0.8) !important;
        color: #ffffff !important;
        border: 2px solid rgba(0, 217, 255, 0.3) !important;
        border-radius: 10px !important;
        font-family: 'Exo 2', sans-serif !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #00d9ff !important;
        box-shadow: 0 0 15px rgba(0, 217, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #1e3c72 0%, #2a5298 50%, #00d9ff 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 217, 255, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(0, 217, 255, 0.5) !important;
        background: linear-gradient(45deg, #2a5298 0%, #00d9ff 50%, #ffffff 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02) !important;
    }
    
    /* Video container styling */
    .stVideo {
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 30px rgba(0, 217, 255, 0.3) !important;
        border: 2px solid rgba(0, 217, 255, 0.4) !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background: rgba(5, 10, 25, 0.9) !important;
        border-right: 2px solid rgba(0, 217, 255, 0.3) !important;
    }
    
    /* Metrics and info boxes */
    .stMetric {
        background: rgba(15, 25, 50, 0.6) !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0, 217, 255, 0.3) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1e3c72, #2a5298, #00d9ff) !important;
        border-radius: 10px !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(0, 255, 127, 0.1) !important;
        border: 1px solid rgba(0, 255, 127, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stError {
        background: rgba(255, 0, 100, 0.1) !important;
        border: 1px solid rgba(255, 0, 100, 0.3) !important;
        border-radius: 10px !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 25, 50, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #1e3c72, #00d9ff);
        border-radius: 10px;
        border: 2px solid rgba(15, 25, 50, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #2a5298, #00d9ff);
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main application function"""
    # Apply futuristic styling
    add_futuristic_background()
    
    # Initialize video generator
    video_gen = VideoGenerator()
    
    # App title
    st.title("PEPPO AI VIDEO GENERATOR")
    st.markdown("### Transform your imagination into stunning AI-generated videos")
    
    # Create two columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Video Generation")
        
        # Get available providers
        available_providers = video_gen.get_available_providers()
        
        if not available_providers:
            st.warning("No video providers are configured. Running in demo mode.")
        
        # User input for video prompt
        prompt = st.text_area(
            "Describe your video",
            placeholder="Enter a detailed description of the video you want to generate...",
            help="Be specific and descriptive for better results"
        )
        
        # Video settings
        col_settings1, col_settings2, col_settings3 = st.columns(3)
        
        with col_settings1:
            duration = st.slider("Duration (seconds)", 3, 10, 7)
            
        with col_settings2:
            style = st.selectbox(
                "Video Style",
                ["Cinematic", "Realistic", "Artistic", "Fantasy", "Sci-Fi", "Animation", "Abstract", "Documentary"]
            )
        
        with col_settings3:
            provider = st.selectbox(
                "AI Provider",
                available_providers,
                format_func=lambda x: x.value
            )
        
        # Show provider info
        if provider:
            provider_info = video_gen.get_provider_info(provider)
            if provider_info:
                st.info(f"**{provider_info['name']}**: {provider_info['description']}")
        
        # Generation button
        if st.button("GENERATE VIDEO", type="primary"):
            if prompt:
                # Run async video generation
                video_path = asyncio.run(video_gen.generate_video(prompt, duration, style, provider))
                if video_path:
                    st.session_state.generated_video = video_path
                    st.session_state.video_info = {
                        'prompt': prompt,
                        'duration': duration,
                        'style': style,
                        'provider': provider.value,
                        'generated_at': datetime.now()
                    }
                    st.rerun()
            else:
                st.error("Please enter a video description")
    
    with col2:
        st.markdown("#### Video Preview")
        
        # Display generated video
        if 'generated_video' in st.session_state:
            st.video(st.session_state.generated_video)
            
            # Show video info
            if 'video_info' in st.session_state:
                info = st.session_state.video_info
                st.markdown(f"""
                **Prompt**: {info['prompt'][:50]}...  
                **Duration**: {info['duration']}s  
                **Style**: {info['style']}  
                **Provider**: {info['provider']}  
                **Generated**: {info['generated_at'].strftime('%H:%M:%S')}
                """)
            
            # Download button
            try:
                with open(st.session_state.generated_video, 'rb') as file:
                    st.download_button(
                        label="DOWNLOAD VIDEO",
                        data=file.read(),
                        file_name=f"peppo_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                        mime="video/mp4"
                    )
            except:
                # For demo videos that are URLs
                st.markdown(f"[Download Video]({st.session_state.generated_video})")
        else:
            st.info("Your generated video will appear here")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #888; font-family: Exo 2;'>"
        "Powered by Peppo AI Engineering | Next-Generation Video Creation"
        "</div>", 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    # Set page configuration
    st.set_page_config(
        page_title="Peppo AI Video Generator",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    main()
