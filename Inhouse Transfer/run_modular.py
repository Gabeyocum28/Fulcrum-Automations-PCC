#!/usr/bin/env python3
"""
Modular Fulcrum Automation Launcher
Launches the new modular architecture instead of the old monolithic processor
"""

import sys
import os
from pathlib import Path

# Add the src directory to the path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Main entry point for the modular system"""
    try:
        print("🚀 Launching Fulcrum Automation - Modular Architecture")
        print("="*60)
        
        # Check if src directory exists
        if not src_path.exists():
            print("❌ Error: src directory not found!")
            print("Please ensure the modular architecture is properly set up.")
            return
        
        # Import and run the orchestrator
        from main_orchestrator import main as run_orchestrator
        run_orchestrator()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all required modules are available in the src directory.")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("Please check the error and try again.")

if __name__ == "__main__":
    main()
