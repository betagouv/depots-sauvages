import logging
import tempfile
from pathlib import Path

import convertapi
from django.conf import settings

logger = logging.getLogger(__name__)


def configure_convertapi():
    """
    Configure the ConvertAPI client with settings.
    """
    if not settings.CONVERTAPI_SECRET:
        logger.warning("ConvertAPI in not configured. PDF conversion will be disabled.")
        return False
    convertapi.api_credentials = settings.CONVERTAPI_SECRET
    return True


def convert_odt_to_pdf(odt_path, output_filename):
    """
    Convert an ODT file to PDF using ConvertAPI.
    Returns the PDF data as bytes if successful, None otherwise.
    """
    if not configure_convertapi():
        return None
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_pdf_path = Path(temp_dir) / output_filename
            pdf_path = str(temp_pdf_path)
            odt_path = str(odt_path)
            convertapi.convert("pdf", {"File": odt_path}, from_format="odt").save_files(pdf_path)
            # Read the generated PDF
            with open(temp_pdf_path, "rb") as f:
                return f.read()
    except Exception as e:
        logger.error(f"Error converting ODT to PDF: {e}", exc_info=True)
        return None
