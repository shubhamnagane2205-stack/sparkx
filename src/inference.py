import streamlit as st
from ai_edge_litert.interpreter import Interpreter
import numpy as np
from src.preprocessing import prepare_video_frame_for_inference


@st.cache_resource
def get_interpreter(model_path: str) -> Interpreter:
    #Loads and allocates the TFLite interpreter once per app session.
    interpreter=Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter

def _run_single_inference(interpreter: Interpreter,input_array:np.ndarray) ->np.ndarray:
    """
    Runs one forward pass. input_array must already be preprocessed and
    batched, shape (1, H, W, 3), dtype float32.
    """

    input_details=interpreter.get_input_details()
    output_details=interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'],input_array)
    interpreter.invoke()
    output=interpreter.get_tensor(output_details[0]['index'])
    return output[0]

def predict_image(interpreter: Interpreter,input_array: np.ndarray,class_names:list):
    #Single-image prediction.

    probabilities=_run_single_inference(interpreter,input_array)
    predicted_idx=int(np.argmax(probabilities))
    predicted_class=class_names[predicted_idx]
    confidence = float(probabilities[predicted_idx])
    all_probabilities={
        name: float(score) for name,score in zip(class_names,probabilities)
    }
    return predicted_class,confidence,all_probabilities

def predict_video(interpreter: Interpreter,frames:list,image_size: tuple,class_names: list):
    #Video prediction via soft voting
    probability_sum=None
    for frame in frames:
        input_array=prepare_video_frame_for_inference(frame,image_size)
        probabilities=_run_single_inference(interpreter,input_array)
        probability_sum=probabilities if probability_sum is None else probability_sum+probabilities
    averaged_probabilities=probability_sum/len(frames)
    predicted_idx = int(np.argmax(averaged_probabilities))
    predicted_class = class_names[predicted_idx]
    confidence = float(averaged_probabilities[predicted_idx])
    all_probabilities = {
        name: float(prob) for name, prob in zip(class_names, averaged_probabilities)
    }
    return predicted_class, confidence, all_probabilities