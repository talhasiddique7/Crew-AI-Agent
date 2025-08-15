"""
Main entry point for CrewAI AI Assistant
Launches the Streamlit UI by default, with options for FastAPI.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point - defaults to Streamlit UI."""
    print("🚀 Starting CrewAI AI Assistant...")
    print("📺 YouTube summarizer and 🎓 Academic assistant ready!")
    print("🎨 Launching Streamlit UI...")
    print("💡 For FastAPI server, use: python launcher.py fastapi")
    print("🔗 For both UI and API, use: python launcher.py both")
    print("-" * 50)
    
    # Import and run Streamlit app
    from src.ui.streamlit_app import main as streamlit_main
    streamlit_main()

if __name__ == "__main__":
    main()
