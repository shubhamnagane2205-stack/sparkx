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

    # ---- 01 Problem Framing ----
    st.html(render_process_header(
        "problem", "01", "Problem Framing",
        "Spark testing is a fast, century-old way to read steel grade by "
        "eye -- but doing it well takes years of experience. SparkX "
        "exists to automate that read, reliably.",
    ))
    with st.expander("Read more"):
        st.write(
            "Spark testing is a shop-floor technique metallurgists and "
            "machinists have used for over a century to identify a piece "
            "of ferrous metal's composition without lab equipment. "
            "Pressing the metal against a grinding wheel throws off a "
            "stream of sparks, and the color, brightness, length, and "
            "branching pattern of that stream encode real information "
            "about the material's carbon content and alloying elements. "
            "It's fast and needs no special equipment, but reading it "
            "accurately takes years of hands-on training, and even "
            "experienced testers disagree on borderline cases.\n\n"
            "SparkX sets out to automate that read: a computer-vision "
            "system that takes a spark-test image or live video and "
            "identifies the material's class, giving a fast, consistent "
            "second opinion where an expert may not be available. That "
            "framed two separate engineering problems. The first was "
            "deciding what the system should actually be asked to "
            "predict. Steel grading standards define dozens of "
            "near-identical grade codes -- asking a model (or a human) "
            "to name one exact code from a spark pattern alone would "
            "manufacture confident-sounding answers the physical signal "
            "can't actually support. So classes were defined at the "
            "resolution spark testing can reliably distinguish: families "
            "of grades that share the metallurgical traits actually "
            "visible in a spark stream, rather than the full depth of "
            "the grading standard."
        )

    # ---- 02 Data Collection & Class Design ----
    st.html(render_process_header(
        "data", "02", "Data Collection & Class Design",
        "Certified spark-test footage from Yamamoto Scientific Tool "
        "Laboratory gave trustworthy ground-truth labels; grades were "
        "grouped into 9 spark-behavior families.",
    ))
    with st.expander("Read more"):
        st.write(
            "No public dataset exists for spark-pattern classification -- "
            "this was confirmed directly by searching before starting, "
            "and it shaped the whole data strategy. Building one from "
            "scrap metal was ruled out early: without knowing a scrap "
            "sample's actual composition, any label attached to it would "
            "be a guess, and a model trained on guessed labels can only "
            "ever be as reliable as the guess.\n\n"
            "Instead, the dataset is built on certified spark-test footage "
            "from **Yamamoto Scientific Tool Laboratory (YSTL)**, a "
            "Japanese supplier of spark-test reference standards used in "
            "metallurgical training. Each YSTL video shows a spark test "
            "performed on a sample of known, certified composition, "
            "following JIS (Japanese Industrial Standard) spark-test "
            "conventions that have been used in industry since 1966. "
            "That certification is what makes the resulting labels "
            "trustworthy: every training example traces back to a "
            "material whose grade is documented, not inferred by eye.\n\n"
            "Each source video carried an on-screen JIS grade label baked "
            "into the footage. Before any of it could be used for "
            "training, that label was cropped out with ffmpeg -- "
            "otherwise the model could learn to read the on-screen text "
            "instead of the spark pattern itself, which would look like "
            "strong accuracy on this dataset while learning nothing "
            "transferable. Individual grade segments were then "
            "timestamped and extracted from the source videos into a "
            "structured, grade-labeled manifest.\n\n"
            "From there, grades were grouped into class families rather "
            "than kept as individual codes. The first pass produced 9 "
            "classes: three carbon-steel bands by carbon content "
            "(low/medium/high), alloy tool steel, alloy structural "
            "steel, stainless steel, high-speed steel, and two visually "
            "distinctive \"safety-net\" classes -- pure iron and cast "
            "iron -- kept despite having only a single reference clip "
            "each, because their spark patterns are so visually distinct "
            "from every other class that even limited examples were "
            "enough to learn them reliably."
        )

    # ---- 03 Dataset Preparation ----
    st.html(render_process_header(
        "prep", "03", "Dataset Preparation",
        "Frames were sampled to avoid near-duplicates, split by whole "
        "clip (not by frame) to prevent data leakage, and augmented per "
        "class to close real gaps in the data.",
    ))
    with st.expander("Read more"):
        st.write(
            "A labeled video isn't training data by itself -- it has to "
            "become a set of individual labeled images. Frames were "
            "extracted at 2.5 frames per second per clip: fast enough to "
            "capture genuinely different moments in a spark burst's "
            "evolution, slow enough to avoid harvesting dozens of "
            "near-identical frames a fraction of a second apart, which "
            "would inflate the dataset's size without adding real "
            "information.\n\n"
            "The train/validation split was made at the level of entire "
            "clips, not individual frames, and this distinction mattered "
            "more than it might sound. Frames pulled from the same few "
            "seconds of one grinding pass look almost identical to each "
            "other. If some frames from a clip had landed in training "
            "and others from that same clip had landed in validation, "
            "validation accuracy would have looked misleadingly strong "
            "-- the model would effectively be re-shown a slightly "
            "different copy of an image it had already memorized, not "
            "proving it could generalize to a genuinely new physical "
            "sample. Splitting by whole clip instead means every "
            "validation example comes from a grinding pass the model "
            "never saw any part of.\n\n"
            "Because some classes were backed by far fewer independent "
            "clips than others -- as few as one or two, versus six to "
            "eight for the best-represented classes -- straightforward "
            "random sampling would have taught the model that rarer "
            "classes were simply less likely, regardless of what was "
            "actually in front of the camera. Augmentation (small-angle "
            "rotation, brightness and contrast jitter, mild zoom and "
            "noise) topped up under-represented classes to a workable "
            "training count. Critically, this was sized per class rather "
            "than forced to one uniform target across the board: "
            "manufacturing large volumes of near-identical augmented "
            "copies from a single thin source clip would have taught the "
            "model to recognize its own augmentation artifacts rather "
            "than genuine material variation. Class-weighted loss was "
            "layered on top during training as a second, complementary "
            "safeguard against the imbalance that remained."
        )

    # ---- 04 Preprocessing Pipeline ----
    st.html(render_process_header(
        "preprocessing", "04", "Preprocessing Pipeline",
        "A tf.data input pipeline built with Keras utilities turned "
        "labeled image folders into correctly scaled, correctly "
        "shuffled training batches.",
    ))
    with st.expander("Read more"):
        st.write(
            "With frames extracted and sorted into class-named folders, "
            "the next problem was feeding them into the model "
            "efficiently and correctly during training -- correctness "
            "here matters as much as speed, since a subtle bug in this "
            "stage can silently cap a model's accuracy without ever "
            "throwing an error.\n\n"
            "`tf.keras.utils.image_dataset_from_directory` handled the "
            "initial loading: it walks the folder structure and infers "
            "each image's class label directly from its parent folder's "
            "name, so the file layout itself doubles as the labeling "
            "mechanism -- no separate label file to keep in sync. As "
            "part of loading, every image was resized to a resolution "
            "matching whichever backbone was being tested, using bicubic "
            "interpolation. Pixel values were then passed through that "
            "backbone's own `preprocess_input` function -- each "
            "pretrained architecture expects a different scaling "
            "convention (MobileNetV2 rescales to [-1, 1]; other "
            "backbones use different ranges or per-channel "
            "normalization), so the pipeline took the image size and "
            "preprocessing function as configuration rather than hard-"
            "coding either, letting a new candidate architecture be "
            "swapped in for comparison without rewriting the pipeline "
            "itself. Whichever backbone was in use, this step was never "
            "optional or approximate: a backbone's pretrained weights "
            "were learned against inputs scaled exactly one specific "
            "way, so any mismatch here would quietly degrade how useful "
            "its pretrained features are, even though nothing would "
            "crash or warn about it.\n\n"
            "From there, a `tf.data.Dataset` pipeline handled shuffling, "
            "batching, caching and prefetching for training -- and the "
            "order these operations happen in is not just a performance "
            "detail. Shuffling has to happen on individual images, "
            "before they're grouped into batches; shuffling after "
            "batching only reorders which batches come first, while the "
            "images trapped together inside each batch stay fixed "
            "together for every single epoch of training, which quietly "
            "weakens the randomness that effective training depends on. "
            "Caching was placed before shuffling too, so each epoch "
            "could reuse already-decoded images rather than repeating "
            "expensive disk reads, without freezing the shuffle order "
            "in the process."
        )
    # ---- 05 Model Training ----
    st.html(render_process_header(
        "training", "05", "Model Training",
        "Multiple pretrained backbones were compared in TensorFlow/"
        "Keras; fine-tuning consistently hurt every one, so the final "
        "model trains only a lightweight head on a frozen MobileNetV2.",
    ))
    with st.expander("Read more"):
        st.write(
            "Training used transfer learning: rather than training a "
            "convolutional network from scratch, which would need a "
            "dataset far larger than this project's, each candidate "
            "architecture started from weights already trained on "
            "ImageNet, a large general-purpose image dataset. That "
            "pretrained network already knows how to recognize edges, "
            "textures and shapes -- the training here only had to teach "
            "it the much narrower, specific task of distinguishing spark "
            "patterns, which needs far less data than starting from "
            "nothing.\n\n"
            "MobileNetV2, EfficientNetB0 and other backbones were "
            "trained in TensorFlow/Keras, each with its convolutional "
            "base frozen, a GlobalAveragePooling layer, a dropout layer "
            "for regularization, and a final softmax layer producing one "
            "probability per material class, trained with class-weighted "
            "loss to account for the dataset's remaining imbalance.\n\n"
            "The standard next step in transfer learning is fine-tuning: "
            "unfreezing some of the pretrained backbone's own layers and "
            "letting them adjust slightly to the new task, usually "
            "improving accuracy further. That step was tried across "
            "every architecture here, and it consistently made both "
            "training and validation accuracy worse, even at very low "
            "learning rates and with batch normalization correctly held "
            "in inference mode throughout. That pattern -- accuracy "
            "dropping on data the model had already seen, not just on "
            "new data -- is a signature of catastrophic forgetting: the "
            "network has enough newly-unlocked capacity to start "
            "overwriting the general-purpose features it started with, "
            "without enough independent training examples per class to "
            "safely relearn something better in their place. Recognizing "
            "this pattern meant abandoning fine-tuning rather than "
            "continuing to chase it, and pushing accuracy instead "
            "through a fully frozen backbone, a higher 448x448 input "
            "resolution -- large enough to preserve the thin, fine "
            "detail in a spark line that would otherwise blur away at a "
            "more typical 224x224 input -- and a staged learning-rate "
            "schedule that stepped down from 1e-3 to 1e-5 and finally "
            "1e-6 as training progressed.\n\n"
            "Under this frozen-backbone approach, MobileNetV2 produced "
            "the strongest validation accuracy of every architecture "
            "compared, and it's what SparkX ships with: a frozen "
            "MobileNetV2 backbone at 448x448 input resolution, "
            "GlobalAveragePooling2D, a 35% dropout layer, and a 10-way "
            "softmax head, trained end-to-end with the Adam optimizer "
            "through that same staged learning-rate schedule, with no "
            "backbone layers ever unfrozen."
        )
    # ---- 06 Evaluation & Iteration ----
    st.html(render_process_header(
        "evaluation", "06", "Evaluation & Iteration",
        "A confusion matrix -- a table of predicted vs. true labels -- "
        "showed one class was internally inconsistent; splitting it "
        "raised that class's recall from 20.8% to 82.2%.",
    ))
    with st.expander("Read more"):
        st.write(
            "Overall accuracy alone doesn't reveal which specific "
            "classes a model struggles with, or why -- for that, a "
            "confusion matrix is the standard tool: a table with true "
            "labels down one side and predicted labels across the top, "
            "where each cell shows how many times the model predicted a "
            "given class for a given true label. A perfect model would "
            "have every count sitting on the diagonal; anything off the "
            "diagonal is a specific, traceable mistake.\n\n"
            "The first trained model's confusion matrix showed something "
            "more specific than generic noise: the majority of one "
            "class's true examples -- plain high-carbon steel -- were "
            "being predicted as alloy tool steel, a completely different "
            "family. That concentration pointed to a labeling problem "
            "rather than a model weakness: the original "
            "`high carbon steel` class had bundled together plain "
            "high-carbon steel (grades S50C/S55C) and carbon *tool* "
            "steel (grades SK85/SK105), on the assumption that similar "
            "carbon content would mean similar spark behavior. It "
            "doesn't -- tool-grade steel goes through a hardening heat "
            "treatment that plain carbon steel doesn't, and that "
            "treatment changes the spark pattern enough that the model "
            "was, in effect, being asked to learn one label for two "
            "visually different things.\n\n"
            "The class was split into a cleaner `high carbon steel` and "
            "a new `carbon tool steel`, and the model was retrained on "
            "the revised class set. That single change took "
            "`high carbon steel`'s recall from 20.8% to 82.2%, and it "
            "surfaced a smaller, more sensible residual confusion in its "
            "place: `carbon tool steel` is now sometimes mistaken for "
            "`alloy tool steel` -- both genuinely tool-grade steels, "
            "where the shared heat treatment plausibly drives more of "
            "the spark behavior than the alloy content does. Current "
            "evaluation metrics from that revised model are below."
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

    # ---- 07 Deployment Engineering ----
    st.html(render_process_header(
        "deployment", "07", "Deployment Engineering",
        "The trained model was converted to TensorFlow Lite; matching "
        "training-time preprocessing required testing OpenCV against "
        "Pillow directly, since the two libraries' bicubic "
        "implementations aren't identical.",
    ))
    with st.expander("Read more"):
        st.write(
            "A model trained in TensorFlow/Keras carries the full "
            "TensorFlow runtime as a dependency by default -- several "
            "gigabytes, and far more than a deployed app serving one "
            "trained model actually needs. TensorFlow Lite exists "
            "specifically to solve this: it's a lightweight model format "
            "and runtime built for exactly this kind of deployment. The "
            "trained Keras model was converted to a `.tflite` file, "
            "served at inference time through **ai-edge-litert**, "
            "Google's current maintained lightweight interpreter, "
            
            "so the deployed app never needs to install TensorFlow "
            "itself.\n\n"
            "Converting the model was the easy part. Once inference runs "
            "outside the original TensorFlow/Keras environment, every "
            "preprocessing step used during training -- the resize, the "
            "pixel scaling -- has to be reimplemented independently, "
            "without TensorFlow available to do it automatically. That "
            "reimplementation turned out to hide a real risk: \"bicubic "
            "resize\" is not one single, interchangeable operation -- "
            "different libraries implement the bicubic kernel slightly "
            "differently, and those small differences can matter. "
            "Pillow and OpenCV were tested head-to-head by running the "
            "same held-out validation images through the deployed "
            "pipeline with each library and comparing the result back "
            "to the original TensorFlow-based accuracy. Pillow's "
            "bicubic resize measurably reduced accuracy; OpenCV's "
            "matched the original numbers, so OpenCV was adopted for "
            "deployment. That choice came with its own trap to manage: "
            "OpenCV's native pixel order is BGR, not RGB, and every "
            "entry point into the deployed preprocessing code explicitly "
            "converts color order before scaling. That check mattered "
            "more here than it would in a typical vision task, because "
            "spark **color** is part of what the model actually learned "
            "to classify on -- a channel-order mistake wouldn't just "
            "add generic noise, it would systematically scramble the "
            "exact signal the model relies on.\n\n"
            "Two further deployment trade-offs were tested empirically "
            "rather than assumed. Post-training INT8 quantization -- a "
            "standard technique for shrinking a model and speeding up "
            "inference by storing its weights at lower numeric precision "
            "-- was benchmarked and rejected: it dropped validation "
            "accuracy from roughly 79% to 66%, too large a cost for this "
            "task, so the deployed model runs at full float32 precision. "
            "And batched inference was compared against processing video "
            "frames one at a time; the TFLite runtime's CPU delegate "
            "showed no real speed benefit from batching, while "
            "single-frame processing kept peak memory lower -- relevant "
            "if someone evaluates the app on a phone or a modest laptop "
            "rather than a dedicated GPU machine -- so video frames are "
            "processed sequentially."
        )

    # ---- 08 Application Development ----
    st.html(render_process_header(
        "app", "08", "Application Development",
        "The deployed app skips the full TensorFlow dependency, "
        "averages predictions across sampled video frames instead of "
        "taking a single vote, and validates uploads by content, not "
        "filename.",
    ))
    with st.expander("Read more"):
        st.write(
            "The application layer carries forward the same "
            "dependency-light approach as the deployment step before "
            "it: no TensorFlow at runtime, only ai-edge-litert for "
            "inference, OpenCV for reading video frames and resizing "
            "(OpenCV's interpolation is used for every resize, whether "
            "the input is an uploaded image or a sampled video frame -- "
            "not just for video), and Pillow and NumPy for image "
            "decoding and array handling -- a smaller footprint that "
            "starts faster and avoids version conflicts on a "
            "constrained hosting environment.\n\n"
            "Classifying a video means classifying more than one frame, "
            "and how those per-frame predictions get combined matters. "
            "Rather than sampling frames and taking a simple majority "
            "vote of each frame's single predicted label, the app "
            "averages every sampled frame's full probability "
            "distribution across all classes and takes the class with "
            "the highest average -- a technique called soft voting. The "
            "distinction is not cosmetic: a hard vote treats a frame the "
            "model is 51% confident about identically to one it's 95% "
            "confident about, while soft voting lets the more confident "
            "frames carry proportionally more weight in the final "
            "answer, which is strictly more information than a vote "
            "count alone provides.\n\n"
            "Uploaded files are validated by content, not by trusting "
            "the filename's extension: the app attempts to actually "
            "decode whatever was uploaded as the file type it claims to "
            "be before it ever reaches the model, so a corrupted file or "
            "a mislabeled extension is caught early with a clear, "
            "specific error message, rather than surfacing as a "
            "confusing failure deep inside the inference code."
        )
 

    st.markdown("#### Tech stack")
    st.html(render_tech_chips([
        "TensorFlow / Keras", "MobileNetV2", "TensorFlow Lite",
         "OpenCV", "Streamlit", "NumPy", "Pillow",
    ]))

    render_footer()