# 🎬 Peppo AI Video Generator

A Streamlit web application for the Peppo AI Engineering Internship Challenge that generates short AI videos from text prompts.

## 🎯 Challenge Requirements

- ✅ Text input box for user prompts
- ✅ AI video generation (5-10 seconds)
- ✅ Video display in browser
- ✅ Download functionality
- 🚀 Ready for cloud deployment

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
   ```powershell
   git clone <your-repo-url>
   cd Peppo
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Run the app:
   ```powershell
   streamlit run app.py
   ```

4. Open your browser and go to `http://localhost:8501`

## 🔧 Configuration

### API Setup
The app supports multiple AI video generation providers:
- **Runway ML**: Get API key from [Runway ML](https://runwayml.com/)
- **Stable Video Diffusion**: Use Hugging Face or Stability AI
- **Pika Labs**: Get access from [Pika Labs](https://pika.art/)
- **Custom API**: Configure your own endpoint

### Environment Variables (Optional)
Create a `.env` file for default API keys:
```
RUNWAY_API_KEY=your_runway_key
STABILITY_API_KEY=your_stability_key
PIKA_API_KEY=your_pika_key
```

## 🎨 Features

- **Interactive UI**: Clean, modern Streamlit interface
- **Multiple AI Providers**: Support for various video generation APIs
- **Customizable Parameters**: Duration, style, and quality settings
- **Real-time Progress**: Progress tracking during generation
- **Video Preview**: In-browser video playback
- **Download Support**: Save generated videos locally

## 🌐 Deployment

### Render (Recommended)
1. Fork this repository
2. Connect to Render
3. Add environment variables
4. Deploy!

### Railway
```powershell
railway login
railway init
railway up
```

### Vercel
```powershell
vercel --prod
```

### AWS/GCP/Azure
See deployment guides in `/docs` folder.

## 📝 API Integration

Replace the demo functions in `app.py` with actual API calls:

```python
def call_runway_api(prompt, api_key, duration, style):
    # Your Runway ML integration
    pass
```

## 🔒 Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Validate all user inputs
- Implement rate limiting for production

## 🐛 Troubleshooting

### Common Issues
- **API Key Error**: Verify your API key is correct
- **Video Not Loading**: Check file permissions and paths
- **Slow Generation**: Video AI APIs can take 1-5 minutes

### Support
- Check the logs in Streamlit
- Verify internet connection
- Ensure API credits are available

## 📊 Performance

- **Generation Time**: 30 seconds - 5 minutes (depending on API)
- **Video Quality**: Up to 1080p (API dependent)
- **File Size**: 5-50MB per video

## 🏆 Challenge Submission

1. ✅ Live app link: `[Your deployed URL]`
2. ✅ GitHub repository: `[Your repo URL]`
3. ✅ Demo video: Show app functionality
4. ✅ Documentation: This README

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- AI video generation API providers
- Peppo for the internship opportunity

---

**Made with ❤️ for the Peppo AI Engineering Internship Challenge**
