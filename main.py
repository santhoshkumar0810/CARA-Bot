import os
import sys
import subprocess

def main():
    """
    Main entry point for CARA-Bot.
    Launches the Streamlit UI.
    """
    print("Starting CARA-Bot Legal AI...")
    
    app_path = os.path.join(os.path.dirname(__file__), 'ui', 'app.py')
    
    if not os.path.exists(app_path):
        print(f"Error: UI file not found at {app_path}")
        return
        
    print(f"Launching Streamlit app: {app_path}")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], check=True)
    except KeyboardInterrupt:
        print("\nStopping CARA-Bot...")

if __name__ == "__main__":
    main()
