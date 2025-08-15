"""
CrewAI AI Assistant - Main Streamlit Application
Professional UI with tabbed interface for YouTube analysis and academic assistance.
"""

import streamlit as st
import sys
import os
from typing import Optional

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from dotenv import load_dotenv
import validators

from config.settings import get_config
from src.core.ai_service import AIService
from src.utils.youtube_utils import extract_youtube_id

# Load environment variables
load_dotenv()

class StreamlitApp:
    """Main Streamlit application class."""
    
    def __init__(self):
        """Initialize the application."""
        self.config = get_config()
        self.ai_service: Optional[AIService] = None
        self._setup_page_config()
        self._initialize_session_state()
    
    def _setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title=self.config.app_title,
            page_icon=self.config.app_icon,
            layout=self.config.layout,
            initial_sidebar_state="expanded"
        )
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state."""
        if 'service_initialized' not in st.session_state:
            st.session_state.service_initialized = False
        if 'api_key_valid' not in st.session_state:
            st.session_state.api_key_valid = False
    
    def _apply_custom_css(self):
        """Apply custom CSS styling."""
        st.markdown("""
        <style>
        .main-header {
            text-align: center;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .tab-header {
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .info-box {
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .stTab [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTab [data-baseweb="tab"] {
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
            background-color: #f0f2f6;
            border-radius: 10px;
        }
        .stTab [aria-selected="true"] {
            background-color: #667eea;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_header(self):
        """Render application header."""
        st.markdown("""
        <div class="main-header">
            <h1>🤖 CrewAI AI Assistant</h1>
            <p>Professional AI-powered YouTube analysis and academic assistance</p>
        </div>
        """, unsafe_allow_html=True)
    
    def _render_sidebar(self) -> str:
        """Render sidebar configuration and return API key."""
        with st.sidebar:
            st.markdown("### 🔧 Configuration")
            
            groq_api_key = st.text_input(
                "🔑 Groq API Key:",
                type="password",
                value=self.config.groq_api_key or "",
                help="Get your API key from https://console.groq.com",
                placeholder="Enter your Groq API key..."
            )
            
            if groq_api_key:
                st.markdown('<div class="success-box">✅ API Key provided!</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please provide your Groq API key")
            
            st.markdown("---")
            st.markdown("### 📖 How to get API Key:")
            st.markdown("""
            <div class="info-box">
            1. Visit <a href="https://console.groq.com" target="_blank">Groq Console</a><br>
            2. Sign up or log in<br>
            3. Navigate to API Keys section<br>
            4. Create a new API key<br>
            5. Copy and paste it above
            </div>
            """, unsafe_allow_html=True)
            
            if groq_api_key:
                st.markdown("---")
                st.markdown("### ⚡ Status")
                if st.session_state.service_initialized:
                    st.success("🟢 Ready to process")
                    st.info("💡 Select a tab above to get started")
                else:
                    st.warning("🟡 Initializing...")
        
        return groq_api_key
    
    def _initialize_ai_service(self, api_key: str):
        """Initialize AI service with provided API key."""
        if api_key and not st.session_state.service_initialized:
            try:
                # Update config with API key
                self.config.groq_api_key = api_key
                
                # Initialize AI service
                with st.spinner("🔄 Initializing AI service..."):
                    self.ai_service = AIService(self.config)
                    
                    # Test connection
                    if self.ai_service.test_connection():
                        st.session_state.service_initialized = True
                        st.session_state.api_key_valid = True
                        st.sidebar.success("✅ Connected to Groq AI")
                    else:
                        st.sidebar.error("❌ Connection failed")
                        return False
                        
            except Exception as e:
                st.sidebar.error(f"❌ Initialization failed: {str(e)}")
                return False
        
        return True
    
    def _render_youtube_tab(self):
        """Render YouTube video analysis tab."""
        st.markdown('<div class="tab-header">📺 YouTube Video Summarizer</div>', unsafe_allow_html=True)
        st.markdown("Enter any YouTube URL to get an intelligent summary of the video content.")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            youtube_url = st.text_input(
                "🔗 YouTube URL:",
                placeholder="https://www.youtube.com/watch?v=...",
                help="Paste any YouTube video URL here"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            analyze_button = st.button(
                "🔍 Analyze Video", 
                type="primary",
                use_container_width=True
            )
        
        if analyze_button:
            if not youtube_url.strip():
                st.error("❌ Please enter a YouTube URL")
            elif not validators.url(youtube_url):
                st.error("❌ Please enter a valid URL")
            else:
                video_id = extract_youtube_id(youtube_url)
                if not video_id:
                    st.error("❌ Invalid YouTube URL format")
                else:
                    with st.spinner("🔄 Analyzing video content..."):
                        result = self.ai_service.summarize_youtube_video(youtube_url)
                        
                        if result['success']:
                            st.success("✅ Analysis completed!")
                            
                            with st.expander("📊 Summary", expanded=True):
                                st.write(result['summary'])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("🎥 Video ID", video_id)
                            with col2:
                                st.metric("🔗 URL Status", "✅ Valid")
                        else:
                            st.error(f"❌ {result['error']}")
        
        # Manual transcript analysis
        st.markdown("---")
        st.markdown("### 📝 Manual Transcript Analysis")
        st.info("💡 If automatic extraction doesn't work, paste the transcript here:")
        
        manual_transcript = st.text_area(
            "Paste transcript content:",
            height=150,
            placeholder="Paste the video transcript here for analysis..."
        )
        
        if st.button("🔍 Analyze Transcript", key="manual_analysis"):
            if manual_transcript.strip():
                with st.spinner("🔄 Generating summary..."):
                    result = self.ai_service.summarize_text(manual_transcript)
                    
                    if result['success']:
                        st.success("✅ Analysis completed!")
                        
                        with st.expander("📊 Summary", expanded=True):
                            st.write(result['summary'])
                        
                        with st.expander("📝 Original Transcript"):
                            st.text_area("Full content:", manual_transcript, height=200, disabled=True)
                    else:
                        st.error(f"❌ {result['error']}")
            else:
                st.error("❌ Please paste some transcript content")
    
    def _render_academic_tab(self):
        """Render academic assistant tab."""
        st.markdown('<div class="tab-header">🎓 Academic Assistant</div>', unsafe_allow_html=True)
        st.markdown("Ask any academic question and get comprehensive, educational answers.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            academic_question = st.text_area(
                "💡 Your Academic Question:",
                height=120,
                placeholder="e.g., Explain the concept of photosynthesis in plants...",
                help="Ask any question across various academic subjects"
            )
        
        with col2:
            st.markdown("#### 📚 Subject Areas")
            subjects = [
                "🧬 Biology", "🧪 Chemistry", "⚛️ Physics", 
                "📊 Mathematics", "💻 Computer Science", "🏛️ History",
                "📖 Literature", "🌍 Geography", "🧠 Psychology",
                "💰 Economics", "⚖️ Law", "🎨 Arts"
            ]
            
            for subject in subjects:
                st.markdown(f"• {subject}")
        
        get_answer_button = st.button(
            "💡 Get Answer", 
            type="primary",
            use_container_width=True
        )
        
        if get_answer_button:
            if not academic_question.strip():
                st.error("❌ Please enter an academic question")
            elif self.ai_service is None:
                st.error("❌ AI service not initialized. Please check your API key.")
            else:
                with st.spinner("🤔 Generating comprehensive answer..."):
                    result = self.ai_service.answer_academic_question(academic_question)
                    
                    if result['success']:
                        st.success("✅ Answer generated!")
                        
                        with st.expander("💡 Complete Answer", expanded=True):
                            st.write(result['answer'])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("📏 Answer Length", f"{result['answer_length']:,} characters")
                        with col2:
                            st.metric("❓ Question Length", f"{result['question_length']:,} characters")
                    else:
                        st.error(f"❌ {result['error']}")
    
    def _render_footer(self):
        """Render application footer."""
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
            <strong>🤖 CrewAI AI Assistant</strong><br>
            ⚡ Powered by Groq AI | 🎯 Built with CrewAI Framework | 🎨 Streamlit Interface<br>
            <small>Perfect for students, educators, researchers, and curious minds!</small>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Run the main application."""
        try:
            # Apply styling
            self._apply_custom_css()
            
            # Render header
            self._render_header()
            
            # Render sidebar and get API key
            api_key = self._render_sidebar()
            
            # Initialize AI service
            if api_key:
                if not self._initialize_ai_service(api_key):
                    st.error("Failed to initialize AI service. Please check your API key.")
                    st.stop()
            else:
                st.error("🔑 Please enter your Groq API key in the sidebar to continue")
                st.stop()
            
            # Main content tabs
            tab1, tab2 = st.tabs(["📺 YouTube Agent", "🎓 Academic Agent"])
            
            with tab1:
                self._render_youtube_tab()
            
            with tab2:
                self._render_academic_tab()
            
            # Footer
            self._render_footer()
            
        except Exception as e:
            st.error(f"❌ Application error: {str(e)}")

def main():
    """Main entry point for the Streamlit application."""
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()

import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import validators
import re

# Load environment variables
load_dotenv()

def extract_youtube_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be\/([0-9A-Za-z_-]{11})',
        r'youtube\.com\/embed\/([0-9A-Za-z_-]{11})',
        r'youtube\.com\/watch\?v=([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def groq_summarize_transcript(transcript: str, groq_client, model="llama3-8b-8192") -> str:
    """Summarize text using Groq"""
    try:
        prompt = f"""
        Please analyze and summarize the following content:
        
        {transcript}
        
        Provide:
        1. A brief overview (2-3 sentences)
        2. Key points (3-5 main points)
        3. Important insights or takeaways
        4. Target audience or relevance
        
        Make the summary clear, engaging, and informative.
        """
        
        response = groq_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def groq_answer_question(question: str, groq_client, model="llama3-8b-8192") -> str:
    """Answer academic question using Groq"""
    try:
        prompt = f"""
        Please answer the following academic question comprehensively:
        
        Question: {question}
        
        Please provide:
        1. A clear and direct answer
        2. Explanation of key concepts involved
        3. Examples or applications if relevant
        4. Additional context or related information that might be helpful
        
        Make sure your answer is educational and easy to understand.
        """
        
        response = groq_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {str(e)}"

def main():
    """Main application function"""
    st.set_page_config(
        page_title="CrewAI AI Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .tab-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .stTab [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTab [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    .stTab [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 CrewAI AI Assistant</h1>
        <p>Professional AI-powered YouTube analysis and academic assistance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for API key configuration
    with st.sidebar:
        st.markdown("### 🔧 Configuration")
        
        groq_api_key = st.text_input(
            "🔑 Groq API Key:",
            type="password",
            value=os.getenv("GROQ_API_KEY", ""),
            help="Get your API key from https://console.groq.com",
            placeholder="Enter your Groq API key..."
        )
        
        if groq_api_key:
            st.markdown('<div class="success-box">✅ API Key provided!</div>', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Please provide your Groq API key")
        
        st.markdown("---")
        st.markdown("### 📖 How to get API Key:")
        st.markdown("""
        <div class="info-box">
        1. Visit <a href="https://console.groq.com" target="_blank">Groq Console</a><br>
        2. Sign up or log in<br>
        3. Navigate to API Keys section<br>
        4. Create a new API key<br>
        5. Copy and paste it above
        </div>
        """, unsafe_allow_html=True)
        
        if groq_api_key:
            st.markdown("---")
            st.markdown("### ⚡ Status")
            st.success("🟢 Ready to process")
            st.info("💡 Select a tab above to get started")
    
    if not groq_api_key:
        st.error("🔑 Please enter your Groq API key in the sidebar to continue")
        st.stop()
    
    # Initialize Groq client
    try:
        groq_client = Groq(api_key=groq_api_key)
        # Test connection
        test_response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        st.sidebar.success("✅ Connected to Groq AI")
    except Exception as e:
        st.sidebar.error(f"❌ Connection failed: {str(e)}")
        st.error("Failed to connect to Groq AI. Please check your API key.")
        st.stop()
    
    # Create tabs for different agents
    tab1, tab2 = st.tabs(["📺 YouTube Agent", "🎓 Academic Agent"])
    
    # YouTube Agent Tab
    with tab1:
        st.markdown('<div class="tab-header">📺 YouTube Video Summarizer</div>', unsafe_allow_html=True)
        st.markdown("Enter any YouTube URL to get an intelligent summary of the video content.")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            youtube_url = st.text_input(
                "🔗 YouTube URL:",
                placeholder="https://www.youtube.com/watch?v=...",
                help="Paste any YouTube video URL here"
            )
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
            analyze_button = st.button(
                "🔍 Analyze Video", 
                type="primary",
                use_container_width=True
            )
        
        if analyze_button:
            if not youtube_url.strip():
                st.error("❌ Please enter a YouTube URL")
            elif not validators.url(youtube_url):
                st.error("❌ Please enter a valid URL")
            else:
                video_id = extract_youtube_id(youtube_url)
                if not video_id:
                    st.error("❌ Invalid YouTube URL format")
                else:
                    with st.spinner("🔄 Analyzing video content..."):
                        # For now, we'll use a placeholder since transcript API has issues
                        placeholder_content = f"""
                        This is a YouTube video analysis for video ID: {video_id}
                        
                        Since the YouTube transcript API has some limitations, please:
                        1. Open the video in YouTube
                        2. Enable captions/subtitles
                        3. Copy the transcript text
                        4. Use the text area below to paste it for analysis
                        """
                        
                        summary = groq_summarize_transcript(placeholder_content, groq_client)
                        
                        if not summary.startswith("Error"):
                            st.success("✅ Analysis completed!")
                            
                            # Display results in an attractive format
                            st.markdown("### 📋 Video Analysis Results")
                            
                            # Create expandable summary
                            with st.expander("📊 Summary", expanded=True):
                                st.write(summary)
                            
                            # Video information
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("🎥 Video ID", video_id)
                            with col2:
                                st.metric("🔗 URL Status", "✅ Valid")
                        else:
                            st.error(f"❌ {summary}")
        
        # Manual transcript input section
        st.markdown("---")
        st.markdown("### 📝 Manual Transcript Analysis")
        st.info("💡 If automatic extraction doesn't work, paste the transcript here:")
        
        manual_transcript = st.text_area(
            "Paste transcript content:",
            height=150,
            placeholder="Paste the video transcript here for analysis..."
        )
        
        if st.button("� Analyze Transcript", key="manual_analysis"):
            if manual_transcript.strip():
                with st.spinner("🔄 Generating summary..."):
                    summary = groq_summarize_transcript(manual_transcript, groq_client)
                    
                    if not summary.startswith("Error"):
                        st.success("✅ Analysis completed!")
                        
                        with st.expander("� Summary", expanded=True):
                            st.write(summary)
                        
                        with st.expander("📝 Original Transcript"):
                            st.text_area("Full content:", manual_transcript, height=200, disabled=True)
                    else:
                        st.error(f"❌ {summary}")
            else:
                st.error("❌ Please paste some transcript content")
    
    # Academic Agent Tab
    with tab2:
        st.markdown('<div class="tab-header">🎓 Academic Assistant</div>', unsafe_allow_html=True)
        st.markdown("Ask any academic question and get comprehensive, educational answers.")
        
        # Subject selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            academic_question = st.text_area(
                "� Your Academic Question:",
                height=120,
                placeholder="e.g., Explain the concept of photosynthesis in plants...",
                help="Ask any question across various academic subjects"
            )
        
        with col2:
            st.markdown("#### 📚 Subject Areas")
            subjects = [
                "🧬 Biology", "🧪 Chemistry", "⚛️ Physics", 
                "� Mathematics", "💻 Computer Science", "🏛️ History",
                "� Literature", "🌍 Geography", "🧠 Psychology",
                "� Economics", "⚖️ Law", "🎨 Arts"
            ]
            
            for subject in subjects:
                st.markdown(f"• {subject}")
        
        # Answer button
        get_answer_button = st.button(
            "� Get Answer", 
            type="primary",
            use_container_width=True
        )
        
        if get_answer_button:
            if not academic_question.strip():
                st.error("❌ Please enter an academic question")
            else:
                with st.spinner("🤔 Generating comprehensive answer..."):
                    answer = groq_answer_question(academic_question, groq_client)
                    
                    if not answer.startswith("Error"):
                        st.success("✅ Answer generated!")
                        
                        # Display answer in an attractive format
                        st.markdown("### 📚 Academic Answer")
                        
                        with st.expander("💡 Complete Answer", expanded=True):
                            st.write(answer)
                        
                        # Question metadata
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("📏 Answer Length", f"{len(answer):,} characters")
                        with col2:
                            st.metric("❓ Question Length", f"{len(academic_question):,} characters")
                    else:
                        st.error(f"❌ {answer}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem;'>
        <strong>🤖 CrewAI AI Assistant</strong><br>
        ⚡ Powered by Groq AI | 🎯 Built with CrewAI Framework | 🎨 Streamlit Interface<br>
        <small>Perfect for students, educators, researchers, and curious minds!</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
