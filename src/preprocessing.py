
import numpy as np
import cv2
from PIL import Image


def preprocess_input(image_array:np.ndarray) -> np.ndarray:
    x=image_array.astype(np.float32)
    x=(x/127.5)-1.0
    return x

def _resize_and_preprocess(rgb_array:np.ndarray,target_size:tuple) -> np.ndarray:
    resized=cv2.resize(rgb_array,target_size,interpolation=cv2.INTER_CUBIC)
    preprocessed=preprocess_input(resized)
    return np.expand_dims(preprocessed,axis=0)

def prepare_image_for_inference(pil_image:Image.Image,target_size:tuple) -> np.ndarray:
    if pil_image.mode!='RGB':
        pil_image=pil_image.convert("RGB")
    rgb_array=np.array(pil_image)
    return _resize_and_preprocess(rgb_array,target_size)

def prepare_video_frame_for_inference(bgr_frame:np.ndarray,target_size:tuple) -> np.ndarray:
    rgb_array=cv2.cvtColor(bgr_frame,cv2.COLOR_BGR2RGB)
    return _resize_and_preprocess(rgb_array,target_size)
