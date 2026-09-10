import os
import tempfile
import cv2
from PIL import Image,UnidentifiedImageError

from config import (
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_VIDEO_EXTENSIONS,
    MAX_UPLOAD_SIZE_MB,
)


def _get_extension(file_name:str) -> str:
    return file_name.rsplit('.',1)[-1].lower() if '.' in file_name else ''

def _is_valid_image_content(uploaded_file) ->bool:
    try:
        uploaded_file.seek(0)
        img=Image.open(uploaded_file)
        img.verify()
        return True
    except(UnidentifiedImageError,OSError):
        return False
    finally:
        uploaded_file.seek(0)


def _is_valid_video_content(uploaded_file) ->bool:
    tmp_path=None
    cap=None

    try:
        uploaded_file.seek(0)
        extension=_get_extension(uploaded_file.name)
        with tempfile.NamedTemporaryFile(delete=False,suffix='.'+extension) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path=tmp_file.name

        cap=cv2.VideoCapture(tmp_path)
        is_open=cap.isOpened()
        has_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) > 0 if is_open else False
        return is_open and has_frames
    except Exception:
        return False
    finally:
        if cap is not None:
            cap.release()
        uploaded_file.seek(0)
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


def validate_upload(uploaded_file):
    '''
    Returns (is_valid: bool, file_kind: image | video | None ,error_message: str | None )

    '''
    if uploaded_file is None:
        return False,None,"No file uploaded."

    size_mb=uploaded_file.size/(1024*1024)
    if size_mb>MAX_UPLOAD_SIZE_MB:
        return False,None,(
            f"File is too large ({size_mb:.1f} MB). "
            f"Maximum allowed size is {MAX_UPLOAD_SIZE_MB} MB."
        )
    extension=_get_extension(uploaded_file.name)
    if extension in ALLOWED_IMAGE_EXTENSIONS:
        if _is_valid_image_content(uploaded_file):
            return True,'image',None
        return False,None,(
            
            "This file has an image extension but its content doesn't "
            "look like a valid image. Please check the file and try again."
        )    
    if extension in ALLOWED_VIDEO_EXTENSIONS:
        if _is_valid_video_content(uploaded_file):
            return True,'video',None
        return False,None,(
            "This file has a video extension but its content doesn't "
            "look like a valid, readable video. Please check the file "
            "and try again."
        )

    allowed=sorted(ALLOWED_IMAGE_EXTENSIONS|ALLOWED_VIDEO_EXTENSIONS)  
    return False, None, (
        f"Unsupported file type '.{extension}'. "
        f"Supported types: {', '.join(allowed)}."
    )