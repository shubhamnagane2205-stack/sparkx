import streamlit as st
from PIL import Image
from config import IMAGE_SIZE, CLASS_NAMES, MODEL_PATH, FRAMES_PER_VIDEO
from src.preprocessing import prepare_image_for_inference
from src.validation import validate_upload
from src.inference import predict_image, predict_video, get_interpreter
from src.video_utils import sample_frames





def render_result_card(predicted_class: str, confidence: float) -> str:
    """
    Builds the result card HTML using the CSS classes defined in
    src/styles.py (.result-card, .predicted-class, .confidence-bar-*).
    """
    display_name = predicted_class.replace("_", " ")
    confidence_pct = round(confidence * 100, 1)
    return f"""
    <div class="result-card">
        <p class="predicted-class-label">Predicted Material Class</p>
        <p class="predicted-class">{display_name}</p>
        <div class="confidence-bar-track">
            <div class="confidence-bar-fill" style="width: {confidence_pct}%;"></div>
        </div>
        <p class="confidence-bar-label">Confidence: {confidence_pct}%</p>
    </div>
    """

def main():
    st.title("Spark Test Material Classifier")
    st.write(
        "Upload a spark-test image or video clip to identify the ferrous "
        "material class from its spark pattern."
    )
    uploaded_file = st.file_uploader(
        "Upload an image or video",
        type=["jpg", "jpeg", "png", "mp4", "mov", "avi"],
    )

main()