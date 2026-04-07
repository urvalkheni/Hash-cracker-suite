from pathlib import Path
import sys

# Ensure project root is importable during pytest collection
# across different pytest import modes/environments.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
