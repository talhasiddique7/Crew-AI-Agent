# 🤖 CrewAI AI Assistant

A professional AI-powered application for YouTube video summarization and academic question answering, built with CrewAI framework and Groq AI.

## ✨ Features

### 📺 YouTube Video Analysis
- **Smart URL Parsing**: Extract video IDs from various YouTube URL formats
- **Intelligent Summarization**: AI-powered content analysis and key insights
- **Manual Transcript Support**: Paste transcripts for analysis when auto-extraction isn't available
- **Professional Results**: Structured summaries with key points and insights

### 🎓 Academic Assistant
- **Multi-Disciplinary Support**: Biology, Chemistry, Physics, Mathematics, Computer Science, and more
- **Comprehensive Answers**: Detailed explanations with examples and context
- **Educational Focus**: Designed for students, educators, and researchers
- **Interactive Interface**: Easy-to-use question and answer format

### ⚡ Technical Features
- **Ultra-Fast AI**: Powered by Groq AI for lightning-fast responses
- **Professional UI**: Modern, responsive Streamlit interface with custom styling
- **Secure Configuration**: Environment-based API key management
- **Modular Architecture**: Clean, maintainable code structure
- **Error Handling**: Robust error handling and user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crew-ai
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Add your Groq API key to .env file
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:8501`

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

### Getting a Groq API Key
1. Visit [Groq Console](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and add to your `.env` file

## 📁 Project Structure

```
crew-ai/
├── config/                 # Configuration settings
│   ├── __init__.py
│   └── settings.py         # App configuration
├── src/                    # Source code
│   ├── __init__.py
│   ├── core/              # Core functionality
│   │   ├── __init__.py
│   │   ├── ai_service.py  # Main AI service
│   │   └── groq_llm.py    # Groq LLM wrapper
│   ├── ui/                # User interface
│   │   ├── __init__.py
│   │   └── streamlit_app.py # Streamlit application
│   └── utils/             # Utility functions
│       ├── __init__.py
│       └── youtube_utils.py # YouTube URL processing
├── docs/                  # Documentation
├── scripts/               # Deployment scripts
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🎯 Usage

### YouTube Video Analysis
1. Open the **YouTube Agent** tab
2. Paste any YouTube video URL
3. Click "Analyze Video" for automatic processing
4. Or use the manual transcript section for custom content

### Academic Questions
1. Open the **Academic Agent** tab
2. Type your academic question
3. Click "Get Answer" for comprehensive responses
4. View detailed explanations and examples

## 🛠️ Development

### Running in Development Mode
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with hot reload
streamlit run src/ui/streamlit_app.py

# Or use the main entry point
python main.py
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions and classes
- Maintain modular structure

## 🔍 Troubleshooting

### Common Issues

**API Key Error**
- Ensure your Groq API key is valid and properly set in `.env`
- Check that you have sufficient API credits

**YouTube URL Issues**
- Verify the URL format is correct
- Ensure the video is public and has captions available
- Use the manual transcript feature if automatic extraction fails

**Installation Problems**
- Update pip: `pip install --upgrade pip`
- Use virtual environment to avoid conflicts
- Check Python version compatibility (3.8+)

## 📊 Performance

- **Response Time**: Sub-second responses with Groq AI
- **Concurrent Users**: Supports multiple simultaneous users
- **Scalability**: Modular architecture for easy scaling
- **Resource Usage**: Lightweight and efficient

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the agent framework
- [Groq](https://groq.com/) for ultra-fast AI inference
- [Streamlit](https://streamlit.io/) for the web interface
- Community contributors and users

## 📞 Support

- 📧 Email: [talhasiddique.developer@gmail.com]
- 📚 Docs: [Documentation](./docs/)

---

**Made with ❤️ for students, educators, and curious minds!**
