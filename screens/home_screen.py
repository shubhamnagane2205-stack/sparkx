
import streamlit as st
from PIL import Image
from src.validation import validate_upload
from src.inference import run_inference
from config import (
    LOGO_PATH,
    BACKGROUND_IMAGE_PATH
)
from UI.styles import (
    get_custom_css,
    render_header,
    render_footer,
    render_result_card,
    render_result_placeholder,
    hero_section,
    apply_layout
)


def home_screen():

    apply_layout()
    st.markdown(get_custom_css(), unsafe_allow_html=True)


    render_header(subtitle='AI-powered ferrous material identification',
        logo_path=LOGO_PATH,prime_button_name='Guide',sec_button_name="Metrics",state_pb='guide',state_sb='metric')

    hero_section(path_of_background_image=BACKGROUND_IMAGE_PATH)
    
    st.markdown(
        """
        <div class="sparkx-section-heading">
            <span class="sparkx-section-icon">✦</span>
            <h2>Analyze your sample</h2>
            
        </div>
        """,
        unsafe_allow_html=True,
    )
    left_col, right_col = st.columns([1, 1],vertical_alignment='top',gap='large')

    with left_col:
        st.markdown(
            """
            <div class="sparkx-panel-title">
                <span>Upload</span>
            </div>

            <div class="sparkx-panel-description">
                Upload your spark-test image or video.
            </div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Upload a spark-test image or video",
            type=["jpg", "jpeg", "png", "mp4", "mov", "avi"],
            label_visibility="collapsed",
            accept_multiple_files=False
        )

        if uploaded_file is None:
            st.html(
                    """
                    <style>
                    [data-testid="stFileUploaderDropzone"] {
                        min-height: 220px;
                    }

                    [data-testid="stFileUploaderDropzoneInstructions"] {
                        height: 100%;
                    }
                    </style>
                    """
                )
            st.session_state.pop("result", None)
        else:
            st.session_state.pop("result", None)
            
            is_valid, file_kind, error_message = validate_upload(uploaded_file)

            if not is_valid:
                st.error(error_message)
            else:
                
                if file_kind == "image":
                    image = Image.open(uploaded_file)
                    st.image(image,width='stretch')
                    uploaded_file.seek(0)
                else:
                    st.video(uploaded_file)
                    uploaded_file.seek(0)
                
                if st.button("Analyze Spark Pattern", width='stretch',type='primary'):
                    
        
                    try:
                        with st.spinner("Analyzing spark pattern..."):
                            predicted_class, confidence, all_probs = run_inference(
                                uploaded_file, file_kind
                            )
                    except Exception as e:
                        st.error(str(e)
                    
                )   
                    else:
                        st.session_state["result"] = {
                            "predicted_class": predicted_class,
                            "confidence": confidence,
                        }
                    

    with right_col:
        st.markdown(
            """
            <div class="sparkx-panel-title">
                <span>Result</span>
            </div>

            <div class="sparkx-panel-description">
                Material identification result.
            </div>
            """,
            unsafe_allow_html=True,
        )
        result = st.session_state.get("result")
        if result:
            st.html(
                render_result_card(result["predicted_class"], result["confidence"])
                
            )
        else:
            st.html(render_result_placeholder())

    render_footer()


