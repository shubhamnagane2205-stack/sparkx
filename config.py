#Centralized constants.

MODEL_PATH = "models/SparkLite.tflite"
IMAGE_SIZE = (448, 448)

#The model's output indices map to list's indices
CLASS_NAMES = [
    "alloy_structural_steel",
    "alloy_tool_steel",
    "carbon_tool_steel",
    "cast_iron",
    "high_carbon_steel",
    "high_speed_steel",
    "low_carbon_steel",
    "medium_carbon_steel",
    "pure_iron",
    "stainless_steel",
]

FRAMES_PER_VIDEO = 10  # frames sampled per video for soft-voting
 
MAX_UPLOAD_SIZE_MB = 50
 
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "mov", "avi"}