import base64
import io
import logging
import tempfile
from typing import Optional

import filetype
from PIL import Image

logger = logging.getLogger(__name__)

MAX_IMAGE_BYTES = 20 * 1024 * 1024  # 20 MB max

# Canonical mapping from allowed MIME types to output extensions
MIME_TO_EXTENSION = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Decompression Bomb DoS protection
Image.MAX_IMAGE_PIXELS = 25_000_000  # 25 Megapixels max


def save_base64_to_temp_file(photo_data: str) -> Optional[str]:
    """
    Decodes a Base64 string or Data URI and saves it to a temporary file on disk.
    Performs local security validations:
    - Size check
    - Magic bytes format whitelist
    - Structural integrity & Decompression Bomb protection via Pillow
    - Sanitization (re-encoding image stream to strip malformed EXIF / polyglots)
    """
    if not photo_data:
        return None
    base64_str = photo_data.split(",", 1)[1] if "," in photo_data else photo_data
    try:
        img_bytes = base64.b64decode(base64_str)
    except Exception as e:
        logger.error(f"Error decoding base64 image data: {e}")
        return None
    # 1. Size check
    if len(img_bytes) > MAX_IMAGE_BYTES:
        logger.warning(
            f"Image size ({len(img_bytes)} bytes) exceeds maximum limit ({MAX_IMAGE_BYTES} bytes)"
        )
        return None
    # 2. Format & magic bytes check
    kind = filetype.guess(img_bytes)
    if not kind or kind.mime not in MIME_TO_EXTENSION:
        logger.warning(
            f"Rejected unsupported or dangerous file type: {kind.mime if kind else 'Unknown'}"
        )
        return None
    raw_ext = f".{kind.extension}".lower() if kind.extension else ""
    if raw_ext not in ALLOWED_EXTENSIONS:
        logger.warning(f"Rejected unsupported file extension: '{raw_ext}' for MIME '{kind.mime}'")
        return None
    ext = MIME_TO_EXTENSION[kind.mime]
    # 3. Structural integrity check & sanitization via Pillow
    try:
        with Image.open(io.BytesIO(img_bytes)) as img:
            # Verify stream structural integrity
            img.verify()
        # Re-open to load and re-encode clean image (strips EXIF / polyglots)
        with Image.open(io.BytesIO(img_bytes)) as img:
            img.load()
            with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
                save_format = img.format if img.format in ["JPEG", "PNG", "WEBP"] else "JPEG"
                img.save(temp_file, format=save_format)
                return temp_file.name
    except Image.DecompressionBombError:
        logger.error("Decompression bomb detected in image upload!")
        return None
    except Exception as e:
        logger.error(f"Failed image integrity check or sanitization: {e}")
        return None
