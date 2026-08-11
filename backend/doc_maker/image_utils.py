import base64
import logging
import tempfile
from typing import Optional

import filetype

logger = logging.getLogger(__name__)


def save_base64_to_temp_file(photo_data: str) -> Optional[str]:
    """
    Decodes a Base64 string or Data URI and saves it to a temporary file on disk.
    Returns the file path of the created temporary file, or None if decoding or type detection fails.
    """
    if not photo_data:
        return None
    base64_str = photo_data.split(",", 1)[1] if "," in photo_data else photo_data
    try:
        img_bytes = base64.b64decode(base64_str)
    except Exception as e:
        logger.error(f"Error decoding base64 image data: {e}")
        return None
    kind = filetype.guess(img_bytes)
    if not kind:
        logger.warning("Could not detect a valid image format for provided photo data")
        return None
    ext = f".{kind.extension}"
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        temp_file.write(img_bytes)
        return temp_file.name
