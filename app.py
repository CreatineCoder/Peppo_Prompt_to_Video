import streamlit as st
import os
import time
import requests
import tempfile
from pathlib import Path

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
    st.markdown("### Generate AI Videos from Text Prompts")
    st.markdown("---")
    
    # Initialize session state
    if 'video_generated' not in st.session_state:
        st.session_state.video_generated = False
    if 'video_path' not in st.session_state:
        st.session_state.video_path = None
    if 'video_url' not in st.session_state:
        st.session_state.video_url = None
    
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
            ["Realistic", "Animated", "Cinematic", "Abstract"]
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
    if st.session_state.video_generated and st.session_state.video_path:
        st.markdown("---")
        st.subheader("Generated Video")
        
        # Display video
        try:
            if os.path.exists(st.session_state.video_path):
                st.video(st.session_state.video_path)
            elif st.session_state.video_url:
                st.video(st.session_state.video_url)
        except Exception as e:
            st.error(f"Error displaying video: {str(e)}")
        
        # Download button
        with download_col:
            if st.session_state.video_path and os.path.exists(st.session_state.video_path):
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
            <p>Generate amazing videos with AI!</p>
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
    """Generate video using AI API"""
    
    # Internal API configuration - handled behind the scenes
    API_PROVIDER = "Runway ML"  # Default provider - can be configured internally
    API_KEY = os.getenv("VIDEO_API_KEY", "demo-mode")  # Load from environment variables
    
    with st.spinner(f"Generating video... This may take a few minutes."):
        try:
            # Simulate API call - Replace this with actual API integration
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate progress
            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 20:
                    status_text.text("Initializing AI model...")
                elif i < 50:
                    status_text.text("Processing your prompt...")
                elif i < 80:
                    status_text.text("Generating video frames...")
                else:
                    status_text.text("Finalizing video...")
                time.sleep(0.05)  # Simulate processing time
            
            # For demo purposes, create a placeholder video path
            # In production, replace this with actual API call
            demo_video_path = create_demo_video(prompt, duration, style)
            
            st.session_state.video_generated = True
            st.session_state.video_path = demo_video_path
            
            progress_bar.empty()
            status_text.empty()
            st.success("Video generated successfully!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error generating video: {str(e)}")
            st.error("Please try again or contact support if the issue persists.")

def create_demo_video(prompt, duration, style):
    """Create a demo video file (placeholder for actual API integration)"""
    # This is a placeholder function - in production, you would:
    # 1. Call the actual AI video generation API
    # 2. Handle the response and download the video
    # 3. Save it to a temporary location
    
    # For now, return a path to where the video would be saved
    temp_dir = tempfile.gettempdir()
    video_filename = f"peppo_video_{int(time.time())}.mp4"
    video_path = os.path.join(temp_dir, video_filename)
    
    # In a real implementation, you would save the generated video here
    # For demo purposes, we'll just return the path
    return video_path

# API Integration functions (to be implemented based on chosen provider)
def call_runway_api(prompt, api_key, duration, style):
    """Call Runway ML API"""
    # Implement Runway ML API integration
    pass

def call_stable_video_api(prompt, api_key, duration, style):
    """Call Stable Video Diffusion API"""
    # Implement Stable Video Diffusion API integration
    pass

def call_pika_api(prompt, api_key, duration, style):
    """Call Pika Labs API"""
    # Implement Pika Labs API integration
    pass

if __name__ == "__main__":
    main()
