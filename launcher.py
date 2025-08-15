"""
Unified Application Launcher

Launch either Streamlit UI, FastAPI server, or both.
"""

import sys
import os
import argparse
import subprocess
import threading
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_streamlit():
    """Run Streamlit application."""
    print("🎨 Starting Streamlit UI...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "src/ui/streamlit_app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])

def run_fastapi():
    """Run FastAPI server."""
    print("⚡ Starting FastAPI server...")
    subprocess.run([sys.executable, "api_server.py"])

def run_both():
    """Run both Streamlit and FastAPI concurrently."""
    print("🚀 Starting both Streamlit UI and FastAPI server...")
    
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Start Streamlit in main thread
    run_streamlit()

def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="CrewAI AI Assistant - Launch Application"
    )
    parser.add_argument(
        "mode",
        choices=["streamlit", "fastapi", "both"],
        default="both",
        nargs="?",
        help="Application mode to run (default: both)"
    )
    parser.add_argument(
        "--port-streamlit",
        type=int,
        default=8501,
        help="Port for Streamlit (default: 8501)"
    )
    parser.add_argument(
        "--port-fastapi", 
        type=int,
        default=8000,
        help="Port for FastAPI (default: 8000)"
    )
    
    args = parser.parse_args()
    
    # Set environment variables for ports
    os.environ["STREAMLIT_PORT"] = str(args.port_streamlit)
    os.environ["FASTAPI_PORT"] = str(args.port_fastapi)
    
    print("🤖 CrewAI AI Assistant")
    print("=" * 50)
    
    if args.mode == "streamlit":
        print("Mode: Streamlit UI only")
        print(f"URL: http://localhost:{args.port_streamlit}")
        run_streamlit()
    elif args.mode == "fastapi":
        print("Mode: FastAPI server only")
        print(f"URL: http://localhost:{args.port_fastapi}")
        print(f"Docs: http://localhost:{args.port_fastapi}/docs")
        run_fastapi()
    elif args.mode == "both":
        print("Mode: Both Streamlit UI and FastAPI server")
        print(f"Streamlit: http://localhost:{args.port_streamlit}")
        print(f"FastAPI: http://localhost:{args.port_fastapi}")
        print(f"API Docs: http://localhost:{args.port_fastapi}/docs")
        run_both()

if __name__ == "__main__":
    main()
