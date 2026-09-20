import streamlit as st
 
from config import (
    LOGO_PATH,
    GUIDE_CORRECT_ORIENTATION_IMAGE,
    GUIDE_INCORRECT_ORIENTATION_IMAGE,
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_VIDEO_EXTENSIONS,
    MAX_UPLOAD_SIZE_MB,
)
from UI.styles import (
    get_custom_css,
    render_header,
    render_footer,
    apply_layout,
    render_page_heading,
    render_card_row,
    render_orientation_comparison,
)
 
 
def guide_screen():
    apply_layout()
    st.markdown(get_custom_css(), unsafe_allow_html=True)
 
    render_header(
        subtitle="AI-powered ferrous material identification",
        logo_path=LOGO_PATH,
        prime_button_name="Home",
        sec_button_name="Methodology",
        state_pb="home",
        state_sb="methodology",
    )
 
    st.html(render_page_heading(
        "Guide",
        "Everything you need to get an accurate result from SparkX.",
    ))
 
    # How it works
    st.markdown("#### How it works")
    st.html(render_card_row([
        {"badge": "1", "title": "Upload",
         "desc": "Add a spark-test image or video "
                 f"(.{', .'.join(sorted(ALLOWED_IMAGE_EXTENSIONS | ALLOWED_VIDEO_EXTENSIONS))}, "
                 f"up to {MAX_UPLOAD_SIZE_MB}MB)."},
        {"badge": "2", "title": "Preview",
         "desc": "Check the preview to confirm the right file was uploaded."},
        {"badge": "3", "title": "Analyze",
         "desc": "Click Analyze Spark Pattern to run the classifier."},
        {"badge": "4", "title": "Result",
          "desc": "Read the predicted material class and confidence score."},
    ]))
 
    # Orientation
    st.markdown("#### Capture orientation matters")
    
    st.write(
        "SparkX expects sparks flowing in the same direction used during "
        "training. A rotated or flipped capture can reduce accuracy, even "
        "if the material is identified correctly by eye."
    )
    st.html(render_orientation_comparison(
        GUIDE_CORRECT_ORIENTATION_IMAGE,
        GUIDE_INCORRECT_ORIENTATION_IMAGE,
    ))
    
 
    # Getting a good capture 
    st.markdown("#### Getting a good capture")
    st.html(render_card_row([
        {"badge": "\U0001F311", "title": "Dark background",
         "desc": "A plain black or dark background makes the spark stream easiest to read."},
        {"badge": "\U0001F4D0", "title": "Steady angle",
         "desc": "Keep the grinding angle steady for the full capture."},
        {"badge": "\U0001F4A1", "title": "Good lighting",
         "desc": "Avoid glare or heavy shadow directly over the spark stream."},
    ]))
 
    # Understanding your result 
    st.markdown("#### Understanding your result")
    st.write(
        "**Confidence score** reflects how certain the model is about its "
        "top prediction -- higher is better, but a lower score doesn't "
        "necessarily mean the result is wrong, just less certain.\n\n"
        "**Why a material family, not an exact grade?** Spark testing "
        "reliably separates broad material families (e.g. alloy tool "
        "steel vs. low carbon steel), but closely related grades "
        "within one family can look very similar by spark alone. SparkX "
        "reports the family it's confident about, rather than guessing "
        "at a specific grade."
    )
 
    render_footer()
 