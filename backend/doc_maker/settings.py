from pathlib import Path

from backend.settings.base import PROJECT_ROOT

# Define paths relative to this file
CURRENT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = CURRENT_DIR / "doc_templates"

OUTPUT_DIR = PROJECT_ROOT / "documents"
