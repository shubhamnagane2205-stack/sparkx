import json
import streamlit as st

from config import (
    LOGO_PATH,
    METRICS_PATH,
    CLASS_NAMES,
)
from UI.styles import (
    get_custom_css,
    render_header,
    render_footer,
    apply_layout,
    render_page_heading,
    render_timeline_nav,
    render_process_header,
    render_recall_bars,
    render_confusion_matrix_table,
    render_tech_chips,
)


SECTIONS = [
    ("problem", "01", "Problem Framing"),
    ("data", "02", "Data Collection & Class Design"),
    ("prep", "03", "Dataset Preparation"),
    ("preprocessing", "04", "Preprocessing Pipeline"),
    ("training", "05", "Model Training"),
    ("evaluation", "06", "Evaluation & Iteration"),
    ("deployment", "07", "Deployment Engineering"),
    ("app", "08", "Application Development"),
]


def _load_metrics():
    
    try:
        with open(METRICS_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def methodology_screen():
    apply_layout()
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    render_header(
        subtitle="AI-powered ferrous material identification",
        logo_path=LOGO_PATH,
        prime_button_name="Home",
        sec_button_name="Guide",
        state_pb="home",
        state_sb="guide",
    )

    st.html(render_page_heading(
        "Methodology",
        "From raw spark-test footage to a deployed classifier -- the full "
        "engineering process, in the order it actually happened.",
    ))

    st.html(render_timeline_nav([(s[0], f"{s[1]} {s[2]}") for s in SECTIONS]))

    # 01 Problem Framing 
    st.html(render_process_header(
        "problem", "01", "Problem Framing",
        "AI-driven ferrous material identification via spark testing, "
        "with class boundaries chosen for real-world distinguishability, "
        "not JIS-code depth.",
    ))
    with st.expander("Read more"):
        st.write(
            "The brief required classifying material type from spark-test "
            "video/images in real time, with at least five distinguishable "
            "grades. Rather than mapping classes directly onto JIS's deep "
            "grade hierarchy -- dozens of near-identical steel codes -- "
            "classes were designed around spark-behavior families: groups "
            "of grades known to produce visually similar spark patterns "
            "(shared carbon-content band, or shared alloying/heat-treatment "
            "behavior). A human judge evaluating by eye can't reliably "
            "separate two near-identical JIS codes any better than a model "
            "could, so the class boundaries were set where the physical "
            "signal actually changes."
        )

    # 02 Data Collection & Class Design
    st.html(render_process_header(
        "data", "02", "Data Collection & Class Design",
        "Certified JIS-standard reference footage, decoded and organized "
        "into an initial 9-class taxonomy.",
    ))
    with st.expander("Read more"):
        st.write(
            "Reference spark-test videos (JIS C 2504 / G 4404 and related "
            "standards) provided certified, per-grade footage spanning "
            "pure iron, carbon steels, tool steels, alloy steels, "
            "stainless steels, and structural steels -- a trustworthy "
            "ground truth, since each grade's composition is certified "
            "rather than guessed from scrap. Each video's on-screen JIS "
            "grade label was cropped out via ffmpeg, and individual grade "
            "segments were timestamped into a structured manifest before "
            "any class-grouping decisions were made."
        )

    # 03 Dataset Preparation 
    st.html(render_process_header(
        "prep", "03", "Dataset Preparation",
        "Clip-level train/val splitting to prevent leakage, non-redundant "
        "frame sampling, and targeted per-class augmentation.",
    ))
    with st.expander("Read more"):
        st.write(
            "Frames were extracted at 2.5fps per clip -- fast enough to "
            "capture genuinely distinct spark-burst configurations, slow "
            "enough to avoid harvesting near-duplicate frames. Train/val "
            "splits were made at the **clip** level, not the frame level, "
            "so two near-duplicate frames from the same physical grind "
            "could never end up split across train and validation. Classes "
            "backed by very little source footage used a documented "
            "temporal-holdout compromise instead of a true independent "
            "split, and augmentation (small-angle tilt, brightness/contrast "
            "jitter, mild zoom and noise) topped up under-represented "
            "classes to a workable count -- sized per class rather than "
            "forced to a uniform target, to avoid manufacturing false "
            "diversity from too few real source clips."
        )

    # 04 Preprocessing Pipeline
    st.html(render_process_header(
        "preprocessing", "04", "Preprocessing Pipeline",
        "OpenCV resize empirically preserved training accuracy where "
        "PIL's bicubic implementation did not; BGR/RGB handling was "
        "explicitly verified.",
    ))
    with st.expander("Read more"):
        st.write(
            "Two resize backends were benchmarked directly against "
            "validation accuracy: PIL's bicubic implementation measurably "
            "degraded results, while OpenCV's matched the TensorFlow-"
            "trained baseline -- so OpenCV was adopted for the deployed "
            "app on evidence, not assumption. Because OpenCV's native "
            "pixel order is BGR rather than RGB, and spark **color** is a "
            "real part of the classification signal (not just shape), "
            "every preprocessing entry point explicitly converts color "
            "order before scaling -- verified with an automated test that "
            "pushes identical visual content through both the image and "
            "video code paths and confirms the outputs match exactly."
        )

    # 05 Model Training
    st.html(render_process_header(
        "training", "05", "Model Training",
        "Transfer learning in TensorFlow/Keras across multiple backbones; "
        "fine-tuning consistently hurt accuracy, so the final model keeps "
        "the backbone frozen.",
    ))
    with st.expander("Read more"):
        st.write(
            "Candidate architectures (MobileNetV2, EfficientNetB0, and "
            "others) were trained in TensorFlow/Keras using ImageNet-"
            "pretrained backbones, a GlobalAveragePooling head, dropout, "
            "and a softmax output, with class-weighted loss to counter "
            "dataset imbalance. Fine-tuning the last N backbone layers was "
            "tested on every architecture and consistently *reduced* both "
            "train and validation accuracy, even at very low learning "
            "rates and with BatchNorm correctly held in inference mode -- "
            "a symptom of catastrophic forgetting rather than a "
            "implementation bug, most likely caused by limited per-class "
            "footage diversity relative to the added trainable capacity. "
            "The final approach keeps the backbone fully frozen and gains "
            "accuracy instead through higher input resolution (224 -> "
            "448px), dropout tuning, and a longer learning-rate schedule."
        )

    # 06 Evaluation & Iteration
    st.html(render_process_header(
        "evaluation", "06", "Evaluation & Iteration",
        "A first confusion matrix revealed one class was internally "
        "inconsistent; splitting it raised that class's recall from "
        "20.8% to 82.2%.",
    ))
    with st.expander("Read more"):
        st.write(
            "The first trained model's confusion matrix showed the "
            "majority of one class's true samples being predicted as "
            "alloy tool steel -- a specific, concentrated confusion, not "
            "generic noise. This pointed to that class bundling both "
            "plain high-carbon steel (S50C/S55C) and carbon **tool** "
            "steel (SK85/SK105) under one label, despite tool-grade heat "
            "treatment producing a materially different spark signature "
            "from plain carbon steel at the same carbon content. Splitting "
            "the class into `high_carbon_steel` and a new "
            "`carbon_tool_steel`, then retraining, resolved that "
            "confusion and surfaced a smaller, expected residual "
            "confusion between `carbon_tool_steel` and `alloy_tool_steel` "
            "-- both genuinely tool-grade steels, plausibly sharing spark "
            "behavior driven more by heat treatment than by alloy content. "
            "Metrics below are from the current model."
        )

    metrics = _load_metrics()
    if metrics:
        st.markdown(f"**Overall validation accuracy: {metrics['accuracy']*100:.1f}%**")
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.markdown("###### Per-class recall")
            st.html(render_recall_bars(metrics["per_class_recall"]))
        with col2:
            st.markdown("###### Confusion matrix")
            st.html(render_confusion_matrix_table(
                metrics["confusion_matrix"], metrics["class_names"]
            ))
    else:
        st.info("Evaluation metrics export not found yet.")

    # 07 Deployment Engineering
    st.html(render_process_header(
        "deployment", "07", "Deployment Engineering",
        "Converted the trained Keras model to TensorFlow Lite; rejected "
        "INT8 quantization after it cut accuracy from ~79% to ~66%.",
    ))
    with st.expander("Read more"):
        st.write(
            "Once training was complete in TensorFlow/Keras, the model "
            "was exported to TensorFlow Lite, with **ai-edge-litert** as "
            "the runtime -- avoiding a full TensorFlow dependency in the "
            "deployed app. Post-training INT8 quantization was benchmarked "
            "for speed but rejected: it dropped validation accuracy from "
            "~79% to ~66%, an unacceptable trade for this use case, so the "
            "deployed model runs at full float32 precision. Single-frame "
            "inference was also benchmarked against batched inference on "
            "the TFLite runtime; since the CPU delegate showed no "
            "batching benefit and single-frame inference keeps peak "
            "memory lower (relevant if a judge is testing on a phone or "
            "modest laptop), video frames are processed sequentially "
            "rather than batched."
        )

    #08 Application Development
    st.html(render_process_header(
        "app", "08", "Application Development",
        "A dependency-light Streamlit app with soft-voting video "
        "inference and content-based upload validation.",
    ))
    with st.expander("Read more"):
        st.write(
            "The deployed app avoids the full TensorFlow dependency "
            "entirely, using only ai-edge-litert for inference, OpenCV "
            "for video frame sampling, and Pillow/NumPy for image "
            "handling. Video classification uses **soft voting** -- "
            "averaging the softmax probability vector across evenly-"
            "sampled frames, rather than a hard majority vote on "
            "per-frame labels -- since it preserves confidence "
            "information a hard vote would discard. Uploaded files are "
            "validated by actually attempting to decode their content, "
            "not just trusting the file extension, so a mislabeled or "
            "corrupted upload is caught before it ever reaches the model."
        )

    st.markdown("#### Tech stack")
    st.html(render_tech_chips([
        "TensorFlow / Keras", "MobileNetV2", "TensorFlow Lite",
         "OpenCV", "Streamlit", "NumPy", "Pillow",
    ]))

    render_footer()