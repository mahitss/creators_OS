import sys
from pathlib import Path

# Ensure root and apps/api are in sys.path
test_dir = Path(__file__).resolve().parent
api_dir = test_dir.parent
root_dir = api_dir.parent.parent

if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

if str(api_dir) not in sys.path:
    sys.path.insert(0, str(api_dir))
