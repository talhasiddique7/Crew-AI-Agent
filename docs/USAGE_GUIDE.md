# 🤖 CrewAI YouTube Summarizer & Academic Assistant - Usage Guide

## 🎯 What This Application Does

This beginner-friendly agent built with CrewAI can:
- **📺 Summarize YouTube videos** from any URL with intelligent analysis
- **🎓 Answer academic questions** across all subjects with detailed explanations
- **⚡ Use Groq AI** for ultra-fast and high-quality responses

## 🚀 Quick Start

### 1. **Get Your Groq API Key**
   - Visit [Groq Console](https://console.groq.com)
   - Sign up for a free account
   - Navigate to "API Keys" section
   - Create a new API key
   - Copy the key (starts with `gsk_...`)

### 2. **Set Up Your API Key**
   - Option A: Enter it in the sidebar when running the app
   - Option B: Edit the `.env` file and replace `your_groq_api_key_here` with your actual key

### 3. **Run the Application**
   ```bash
   # Navigate to the project directory
   cd "/media/professor/New Volume/Internship-szl/crew-ai"
   
   # Run the simple version (recommended for beginners)
   source .venv/bin/activate && streamlit run app_simple.py
   
   # OR run the full CrewAI version
   source .venv/bin/activate && streamlit run app.py
   
   # OR use the convenient script
   ./run_app.sh
   ```

### 4. **Open in Browser**
   - The app will automatically open at `http://localhost:8501`
   - Or manually open this URL in your browser

## 📺 Using the YouTube Summarizer

### **Supported URL Formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`

### **Steps:**
1. **Enter a YouTube URL** in the left column
2. **Click "Summarize Video"** 
3. **Wait for processing** (transcript fetching + AI analysis)
4. **Review the summary** with:
   - Brief overview
   - Key points
   - Important insights
   - Target audience
5. **View original transcript** (optional, in expandable section)

### **Example URLs to Try:**
- Educational content: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Tutorial videos
- Lectures and presentations
- Documentary content

## 🎓 Using the Academic Assistant

### **Types of Questions You Can Ask:**
- **Science**: "Explain photosynthesis in plants"
- **Mathematics**: "What is calculus and how is it used?"
- **History**: "Describe the causes of World War I"
- **Literature**: "Analyze the themes in Shakespeare's Hamlet"
- **Philosophy**: "What are the main ideas of existentialism?"
- **Technology**: "How does machine learning work?"

### **Steps:**
1. **Type your question** in the right column text area
2. **Click "Get Answer"**
3. **Receive comprehensive response** with:
   - Direct answer
   - Key concept explanations
   - Relevant examples
   - Additional context

## 🛠️ Features Overview

### **YouTube Summarizer Features:**
- ✅ Automatic transcript extraction
- ✅ Intelligent content analysis
- ✅ Structured summaries
- ✅ Key points identification
- ✅ Target audience analysis
- ✅ Original transcript viewing

### **Academic Assistant Features:**
- ✅ Multi-disciplinary knowledge
- ✅ Detailed explanations
- ✅ Educational examples
- ✅ Clear and structured answers
- ✅ Additional context provided

### **Technical Features:**
- ✅ Groq AI integration for speed
- ✅ Clean Streamlit interface
- ✅ Real-time processing
- ✅ Error handling
- ✅ Responsive design

## 🔧 Troubleshooting

### **Common Issues & Solutions:**

#### **"Invalid YouTube URL"**
- ✅ Ensure URL is from YouTube
- ✅ Check URL format (should contain video ID)
- ✅ Make sure video is public

#### **"Error fetching transcript"**
- ✅ Video might not have auto-generated captions
- ✅ Video might be private or restricted
- ✅ Try a different video with available transcripts

#### **"Error connecting to Groq AI"**
- ✅ Check your API key is correct
- ✅ Ensure you have internet connection
- ✅ Verify API key hasn't expired
- ✅ Check Groq service status

#### **"Module not found" errors**
- ✅ Ensure virtual environment is activated
- ✅ Run: `pip install -r requirements.txt`
- ✅ Check Python version compatibility

### **Performance Tips:**
- 🚀 Groq AI provides very fast responses (usually under 3 seconds)
- 🚀 YouTube transcript fetching depends on video length
- 🚀 Longer videos may take slightly more time to process

## 📋 File Structure

```
crew-ai/
├── app.py                 # Full CrewAI version
├── app_simple.py         # Simplified version (recommended)
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
├── README.md           # Project documentation
├── USAGE_GUIDE.md      # This usage guide
├── run_app.sh          # Convenient run script
└── .venv/              # Virtual environment
```

## 🎯 Best Practices

### **For YouTube Summarization:**
- Choose videos with clear audio for better transcripts
- Educational and tutorial content works best
- Videos with auto-generated captions are ideal

### **For Academic Questions:**
- Be specific in your questions
- Ask for examples when needed
- Break complex topics into smaller questions

### **General Usage:**
- Keep your Groq API key secure
- Monitor your API usage limits
- Use the simple version for better stability

## 🔮 Advanced Usage

### **Customization Options:**
- Modify prompts in the source code for different output styles
- Adjust response lengths by changing `max_tokens`
- Experiment with different Groq models

### **Integration Ideas:**
- Export summaries to text files
- Save favorite academic answers
- Integrate with note-taking apps

## 📞 Support

If you encounter any issues:
1. Check this usage guide first
2. Review the troubleshooting section
3. Ensure all dependencies are installed
4. Check Groq API key and service status

## 🎉 Enjoy Learning!

This tool is designed to make learning and content consumption more efficient. Whether you're:
- 📚 A student researching topics
- 🎓 An educator preparing materials
- 🤔 A curious mind exploring new subjects

This CrewAI-powered assistant is here to help! 🚀
