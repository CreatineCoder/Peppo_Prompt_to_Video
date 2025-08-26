# Peppo AI Video Generator

**Internship Task Submission - AI Video Generation App**

A Streaml## Usage

1. **Enter Prompt**: Describe your desired videoapplication that generates videos from text prompts using Stability AI's Stable Video Diffusion with an elegant futuristic interface.

## Task Implementation

- **Text Input**: User-friendly prompt input box  
- **AI Video Generation**: 5-10 second videos using Stability AI  
- **Video Display**: In-browser video playback  
- **Download Feature**: One-click MP4 downloads  
- **Modern UI**: Futuristic sci-fi themed interface  
- **Fallback System**: Demo videos when API unavailable  

## Quick Setup

### Requirements
- Python 3.8+
- Stability AI API Key

### Installation
```bash
# Clone repository
git clone https://github.com/CreatineCoder/Peppo_Prompt_to_Video.git
cd Peppo_Prompt_to_Video

# Install dependencies
pip install -r requirements.txt

# Configure API (optional)
echo "STABILITY_API_KEY=sk-your-key-here" > .env

# Run application
streamlit run app.py
```

### Access
Open `http://localhost:8501` in your browser

## Architecture

```
Project Structure:
├── app.py                      # Main Streamlit app
├── video_generator.py          # Video generation logic  
├── config.py                   # Configuration management
├── api_clients/
│   ├── stability_ai_client.py  # Stability AI integration
│   └── stable_video_client.py  # SVD API client
└── utils/file_handler.py       # File operations
```

## Features

**Core Functionality:**
- Text-to-video generation using Stability AI
- Multiple video styles (Cinematic, Realistic, Fantasy, etc.)
- Duration control (5-10 seconds)
- Real-time generation progress
- Video preview and download

**UI/UX:**
- Futuristic space-themed design
- Animated backgrounds and effects
- Responsive layout
- Clean, intuitive interface

**Technical:**
- Modular architecture
- Error handling with fallbacks
- Session state management
- Temporary file cleanup

## Deployment

**Live Demo:** [Your deployed URL here]

### Deployment Options:
- **Streamlit Cloud**: Connect GitHub repo → Deploy
- **Railway**: `railway up`
- **Render**: Connect repo → Auto-deploy
- **Heroku**: Standard deployment process

## Configuration

### API Integration
The app uses Stability AI's Stable Video Diffusion:
- Generates high-quality images as fallback
- Attempts SVD video generation when available
- Falls back to demo videos when needed

### Environment Variables
```env
STABILITY_API_KEY=sk-your-stability-ai-key
DEBUG=False
MAX_FILE_SIZE=104857600
```

## � Usage

1. **Enter Prompt**: Describe your desired video
2. **Select Style**: Choose from available presets
3. **Set Duration**: Use slider for 5-10 seconds
4. **Generate**: Click to start AI generation
5. **Download**: Save your generated content

### Example Prompts:
- "A cat playing with yarn in a sunny garden"
- "Sunset over mountain peaks with birds flying"
- "Futuristic city with flying cars at night"

## Technical Details

**Frontend:** Streamlit with custom CSS/animations  
**Backend:** Python with async video processing  
**AI Service:** Stability AI Stable Video Diffusion  
**Storage:** Temporary file system with cleanup  
**Deployment:** Cloud-ready with environment configs  

## Performance

- **Generation Time**: 30 seconds - 3 minutes
- **Video Quality**: Up to 1024x576 resolution  
- **File Formats**: MP4 output
- **Fallback**: Demo videos + generated images

## Task Completion

**Deliverables:**
- Functional video generation app
- Clean, modern user interface  
- GitHub repository with documentation
- Deployment-ready configuration
- Error handling and fallbacks

**Technical Skills Demonstrated:**
- Python/Streamlit development
- API integration (Stability AI)
- Async programming
- UI/UX design
- Cloud deployment
- Documentation

---

**Built for Peppo AI Engineering Internship Challenge**  
*Demonstrating full-stack development and AI integration capabilities*
