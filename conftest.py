import sys
from pathlib import Path

# Add the project root to the path so pytest can find app.py
sys.path.insert(0, str(Path(__file__).parent))