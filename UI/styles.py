
import os
import datetime
import streamlit as st
import base64
from pathlib import Path

CUSTOM_CSS = """
<style>


/* ---------- Result card ---------- */
/* Container for the prediction outcome: predicted class + confidence.
   No JIS-grade field by design -- see module docstring. */
.result-card {
    background-color: #1C1C1F;
    border-left: 4px solid #FF9F1C;
    border-radius: 8px;
    padding: 1.5rem 1.75rem;
    margin: 0;
}

.result-card .predicted-class {
    color: #F5F5F0;
    font-size: 1.5rem !important;
    font-weight: 700;
    margin: 0 0 0.25rem 0;
    text-transform: capitalize;
}

.result-card .predicted-class-label {
    color: #A3A3A3;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin: 0 0 0.5rem 0;
}

/* ---------- Confidence bar ---------- */

.confidence-bar-track {
    background-color: #0E0E10;
    border-radius: 6px;
    height: 10px;
    width: 100%;
    overflow: hidden;
    margin-top: 0.5rem;
}

.confidence-bar-fill {
    background-color: #FF9F1C;
    height: 100%;
    border-radius: 6px;
    transition: width 0.4s ease-out;
}

.confidence-bar-label {
    color: #A3A3A3;
    font-size: 0.85rem !important;
    margin-top: 0.35rem;
}



/* ---------- Upload zone ---------- */
/* Restyles Streamlit's native file_uploader drop area border/hover. */
[data-testid="stFileUploaderDropzone"] {
    
    background-color: #1C1C1F;
    border: 2px dashed rgba(163, 163, 163, 0.6);
    border-radius: 8px;
    transition: border-color 0.2s ease-out;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #FF9F1C;
}



/* ---------- Footer ---------- */
.app-footer {
    border-top: 1px solid rgba(163, 163, 163, 0.25);
    margin-top: 3rem;
    padding-top: 1rem;
    text-align: center;
}

.app-footer .footer-copyright {
    color: #A3A3A3;
    font-size: 0.85rem !important;
    margin: 0;
}

.app-footer .footer-stack {
    /* Muted token at 75% opacity: deliberately lighter than
       footer-copyright above it, while still clearing WCAG AA
       (4.74:1, verified) against the base background. */
    color: rgba(163, 163, 163, 0.75);
    font-size: 0.8rem !important;
    margin: 0.2rem 0 0 0;
}

/* =========================================================
   ANALYZE SECTION
   ========================================================= */

.sparkx-section-heading {
    margin-top: 8px;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sparkx-section-icon {
    color: #ff9f1c;
    font-size: 14px;
    line-height: 1;
}

.sparkx-section-heading h2 {
    margin: 0;

    font-size: clamp(24px, 2.2vw, 30px);
    line-height: 1.15;
    font-weight: 700;
    letter-spacing: -0.5px;

    color: #f5f5f0;
}




/* =========================================================
   PANEL HEADINGS
   ========================================================= */

.sparkx-panel-title {
    margin: 0;

    font-size: 21px;
    line-height: 1.2;
    font-weight: 700;

    color: #f5f5f0;
}

.sparkx-panel-description {
    margin-top: 5px;
    margin-bottom: 12px;

    font-size: 11px;
    line-height: 1.4;

    color: #8f8f94;
}


/* =========================================================
   UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {
    margin-top: 0;
}


/* =========================================================
   ANALYZE BUTTON
   ========================================================= */
button[kind="primary"]{
    color: #0E0E10
}

.sparkx-section-heading + div {
    /* Prevent accidental layout targeting */
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .sparkx-section-heading {
        margin-top: 6px;
        margin-bottom: 3px;
    }

    .sparkx-section-heading h2 {
        font-size: 24px;
    }

    

    .sparkx-panel-title {
        font-size: 20px;
    }

    .sparkx-panel-description {
        font-size: 11px;
    }
}

/* =========================================================
   RESULT PLACEHOLDER CARD
   ========================================================= */


.sparkx-result-placeholder {
    min-height: 220px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    box-sizing: border-box;

    padding: 28px 24px;

    border: 1px solid #29292d;
    border-radius: 12px;

    text-align: center;

    background: #151518;
}

.sparkx-result-icon {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 38px;
    height: 38px;

    margin-bottom: 12px;

    border: 1px solid #3a3a3f;
    border-radius: 50%;

    color: #ff9f1c;

    font-size: 17px;
}

.sparkx-result-title {
    font-size: 15px;
    font-weight: 650;

    color: #f5f5f0;
}

.sparkx-result-description {
    max-width: 270px;

    margin-top: 6px;

    font-size: 11px;
    line-height: 1.45;

    color: #8f8f94;
}

/* =========================================================
   UPLOADED FILES
   ========================================================= */


[data-testid="stImage"] img {
        height: 150px !important;
        object-fit: cover;
    }



div[data-testid="stElementContainer"]:has(video[data-testid="stVideo"]) {
    height: 150px !important;
    min-height: 150px !important;
    max-height: 150px !important;
}

video[data-testid="stVideo"] {
    height: 150px !important;
    min-height: 150px !important;
    max-height: 150px !important;
    object-fit: contain !important;
    display: block !important;
}
</style>
"""


def get_custom_css() -> str:
    """Returns the CSS block ready to pass to st.markdown(unsafe_allow_html=True)."""
    return CUSTOM_CSS






def render_header(logo_path: str,subtitle: str,prime_button_name: str,sec_button_name: str,state_pb: str, state_sb: str) -> None:
    
    header=st.container(key="sparkx-header")
    left,right=header.columns([6,1.5],vertical_alignment='center')
    with open(logo_path, "rb") as image_file:
        logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    with left:
        st.html(
            f"""
            <style>

                /* =========================================================
                SparkX Header
                ========================================================= */

                .st-key-sparkx-header {{
                    width: 100%;
                    box-sizing: border-box;

                    display: flex;
                    align-items: center;
                    justify-content: space-between;

                    padding: 10px 16px;

                    min-height: 72px;

                    background: #0E0E10;
                    border: 1px solid #29292D;
                    border-radius: 14px;

                    gap: 24px;
                }}


                /* =========================================================
                Brand
                ========================================================= */

                .sparkx-brand {{
                    min-width: 0;

                    display: flex;
                    align-items: center;

                    flex: 1;
                }}


                .sparkx-logo {{
                    width: 60px;
                    height: 60px;

                    object-fit: contain;
                    flex-shrink: 0;

                    display: block;
                }}


                .sparkx-brand-divider {{
                    width: 1px;
                    height: 36px;

                    margin: 0 22px;

                    background: #36363B;

                    flex-shrink: 0;
                }}


                .sparkx-brand-text {{
                    min-width: 0;
                }}


                .sparkx-wordmark {{
                    margin: 0;

                    font-size: 31px;
                    line-height: 1;

                    font-weight: 750;
                    letter-spacing: -0.8px;

                    color: #F5F5F0;

                    white-space: nowrap;
                }}


                .sparkx-wordmark-accent {{
                    color: #FF9F1C;
                }}


                .sparkx-tagline {{
                    margin-top: 6px;

                    max-width: 420px;

                    font-size: 13px;
                    line-height: 1.3;

                    color: #A3A3A3;
                }}


                

                /* =========================================================
                Medium screens / laptops
                ========================================================= */

                @media (max-width: 1000px) {{

                    .st-key-sparkx-header {{
                        gap: 16px;
                        padding: 9px 14px;
                    }}

                    .sparkx-logo {{
                        width: 56px;
                        height: 56px;
                    }}

                    .sparkx-brand-divider {{
                        margin: 0 16px;
                        height: 34px;
                    }}

                    .sparkx-wordmark {{
                        font-size: 28px;
                    }}

                    .sparkx-tagline {{
                        font-size: 12px;
                        max-width: 330px;
                    }}

                    
                }}


                /* =========================================================
                Tablet
                ========================================================= */

                @media (max-width: 768px) {{

                    .st-key-sparkx-header {{
                        gap: 14px;
                        padding: 10px 12px;
                    }}

                    .sparkx-logo {{
                        width: 52px;
                        height: 52px;
                    }}

                    .sparkx-brand-divider {{
                        margin: 0 12px;
                        height: 30px;
                    }}

                    .sparkx-wordmark {{
                        font-size: 25px;
                    }}

                    .sparkx-tagline {{
                        margin-top: 5px;

                        max-width: 280px;

                        font-size: 11px;
                    }}

                    
                }}


                /* =========================================================
                Mobile
                ========================================================= */

                @media (max-width: 600px) {{

                    .st-key-sparkx-header {{
                        flex-direction: column;
                        align-items: stretch;

                        gap: 12px;

                        padding: 12px;
                    }}

                    .sparkx-brand {{
                        width: 100%;
                    }}

                    .sparkx-logo {{
                        width: 52px;
                        height: 52px;
                    }}

                    .sparkx-brand-divider {{
                        height: 30px;
                        margin: 0 12px;
                    }}

                    .sparkx-wordmark {{
                        font-size: 25px;
                    }}

                    .sparkx-tagline {{
                        max-width: 100%;

                        font-size: 11px;
                        line-height: 1.35;
                    }}

                    
                }}


                /* =========================================================
                Small phones
                ========================================================= */

                @media (max-width: 380px) {{

                    .st-key-sparkx-header {{
                        padding: 10px;
                    }}

                    .sparkx-logo {{
                        width: 48px;
                        height: 48px;
                    }}

                    .sparkx-brand-divider {{
                        margin: 0 9px;
                        height: 28px;
                    }}

                    .sparkx-wordmark {{
                        font-size: 22px;
                    }}

                    .sparkx-tagline {{
                        font-size: 10px;
                    }}

                    
                }}

            </style>


            <!-- =========================================================
                Header
                ========================================================= -->

            <header class="sparkx-header">

                <!-- Brand -->
                <div class="sparkx-brand">

                    <img
                        class="sparkx-logo"
                        src="data:image/png;base64,{logo_base64}"
                        alt="SparkX logo"
                    >

                    <div class="sparkx-brand-divider"></div>

                    <div class="sparkx-brand-text">

                        <div class="sparkx-wordmark">
                            Spark<span class="sparkx-wordmark-accent">X</span>
                        </div>

                        <div class="sparkx-tagline">
                            {subtitle}
                            through spark testing
                        </div>

                    </div>

                </div>


                

            </header>
            """


    
    )
    with right:
        col1,col2=st.columns(2,gap='medium')
        with col1:
            
            if st.button(prime_button_name,type='primary',width='stretch'):
                st.session_state["screen"]=state_pb
                st.rerun()
        with col2:
            if st.button(sec_button_name,width='stretch'):
                st.session_state["screen"]=state_sb
                st.rerun()




def hero_section(path_of_background_image: str):

    # PNG only
    image_data = base64.b64encode(
        Path(path_of_background_image).read_bytes()
    ).decode()

    st.html(
        f"""
        <style>

        /* ==============================
           SPARKX HERO
           ============================== */

        .sparkx-hero {{
            position: relative;
            width: 100%;
            height: 145px;

            display: flex;
            align-items: center;

            box-sizing: border-box;
            overflow: hidden;

            padding: 20px 44px;

            border: 1px solid #29292d;
            border-radius: 16px;

            background-image:
                linear-gradient(
                    90deg,
                    rgba(10, 11, 14, 0.98) 0%,
                    rgba(10, 11, 14, 0.90) 42%,
                    rgba(10, 11, 14, 0.35) 75%,
                    rgba(10, 11, 14, 0.10) 100%
                ),
                url("data:image/png;base64,{image_data}");

            background-size: cover;
            background-position: center right;

            color: #f5f5f0;
        }}


        /* Content */

        .sparkx-hero-content {{
            position: relative;
            z-index: 2;

            max-width: 850px;
        }}


        /* Eyebrow */

        .sparkx-eyebrow {{
            display: flex;
            align-items: center;
            gap: 8px;

            margin-bottom: 8px;

            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1.4px;
            text-transform: uppercase;

            color: #a3a3a3;
        }}

        .sparkx-eyebrow::before {{
            content: "";
            width: 6px;
            height: 6px;

            border-radius: 50%;
            background: #ff9f1c;
        }}


        /* Main heading */

        .sparkx-hero h1 {{
            margin: 0;

            font-size: clamp(25px, 2.2vw, 34px);
            line-height: 1.08;
            font-weight: 750;
            letter-spacing: -0.8px;
        }}

        .sparkx-hero h1 span {{
            color: #ff9f1c;
        }}


        /* Description */

        .sparkx-hero-description {{
            margin-top: 8px;

            font-size: 12px;
            line-height: 1.4;

            color: #a3a3a3;
        }}


        /* Features */

        .sparkx-features {{
            display: flex;
            align-items: center;
            gap: 18px;

            margin-top: 9px;

            font-size: 10px;
            font-weight: 600;

            color: #d5d5d0;
        }}

        .sparkx-feature {{
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }}

        .sparkx-feature::before {{
            content: "";
            width: 5px;
            height: 5px;

            border: 1px solid #ff9f1c;
            border-radius: 50%;
        }}


        /* ==============================
           TABLET
           ============================== */

        @media (max-width: 900px) {{

            .sparkx-hero {{
                height: 140px;
                padding: 18px 28px;

                background-position: center right;
            }}

            .sparkx-hero-content {{
                max-width: 72%;
            }}

            .sparkx-hero h1 {{
                font-size: clamp(22px, 3.2vw, 28px);
            }}

            .sparkx-hero-description {{
                font-size: 11px;
            }}
        }}


        /* ==============================
           MOBILE
           ============================== */

        @media (max-width: 640px) {{

            .sparkx-hero {{
                height: 150px;

                padding: 17px 20px;

                border-radius: 12px;

                background-position: 68% center;

                background-image:
                    linear-gradient(
                        90deg,
                        rgba(10, 11, 14, 0.99) 0%,
                        rgba(10, 11, 14, 0.94) 55%,
                        rgba(10, 11, 14, 0.60) 100%
                    ),
                    url("data:image/png;base64,{image_data}");
            }}

            .sparkx-hero-content {{
                max-width: 100%;
            }}

            .sparkx-eyebrow {{
                margin-bottom: 6px;
                font-size: 8px;
                letter-spacing: 1.1px;
            }}

            .sparkx-eyebrow::before {{
                width: 5px;
                height: 5px;
            }}

            .sparkx-hero h1 {{
                font-size: 21px;
                line-height: 1.12;
                letter-spacing: -0.4px;
            }}

            .sparkx-hero-description {{
                margin-top: 6px;
                font-size: 10px;
                line-height: 1.35;

                max-width: 95%;
            }}

            .sparkx-features {{
                gap: 11px;
                margin-top: 7px;
                font-size: 8px;
            }}

            .sparkx-feature {{
                gap: 4px;
            }}

            .sparkx-feature::before {{
                width: 4px;
                height: 4px;
            }}
        }}


        /* ==============================
           VERY SMALL PHONES
           ============================== */

        @media (max-width: 400px) {{

            .sparkx-hero {{
                height: 145px;
                padding: 15px 17px;
            }}

            .sparkx-hero h1 {{
                font-size: 19px;
            }}

            .sparkx-hero-description {{
                font-size: 9px;
            }}

            .sparkx-features {{
                gap: 8px;
                font-size: 7px;
            }}
        }}

        </style>


        <section class="sparkx-hero" id="hero-scroll-target">

            <div class="sparkx-hero-content">

                <div class="sparkx-eyebrow">
                    AI-POWERED SPARK TESTING
                </div>

                <h1>
                    Identify materials from their
                    <span>spark pattern.</span>
                </h1>

                <div class="sparkx-hero-description">
                    Upload a spark-test image or video and let SparkX
                    analyze the pattern to predict the material in seconds.
                </div>

                <div class="sparkx-features">

                    <div class="sparkx-feature">
                        Fast analysis
                    </div>

                    <div class="sparkx-feature">
                        AI-powered
                    </div>

                    <div class="sparkx-feature">
                        Practical results
                    </div>

                </div>

            </div>

        </section>
        """
    )

def apply_layout():
    st.html(
        """
        <style>

            /* =========================================
               Hide Streamlit default UI
               ========================================= */

            /*#MainMenu,
            footer,
            [data-testid="stHeader"] {
                display: none;
            }

            .block-container {
                padding-top: 0 !important;
            }*/


            /* =========================================
               Responsive application container
               ========================================= */

            [data-testid="stMainBlockContainer"] {
                --page-gutter: clamp(16px, 3vw, 40px);

                width: min(
                    1280px,
                    calc(100% - 2 * var(--page-gutter))
                ) !important;

                max-width: none !important;

                margin-left: var(--page-gutter) !important;
                margin-right: auto !important;

                padding-left: 0 !important;
                padding-right: 0 !important;
            }


            /* =========================================
               Mobile
               ========================================= */

            @media (max-width: 768px) {

                [data-testid="stMainBlockContainer"] {
                    --page-gutter: 16px;

                    width: calc(100% - 32px) !important;
                }

            }

        </style>
        """
    )




def render_footer():
    """Renders the shared footer: copyright line + tech-stack credit."""
    year = datetime.datetime.now().year
    st.markdown(
        f"""
        <div class="app-footer">
            <p class="footer-copyright">&copy; {year} Shubham Nagane. All rights reserved.</p>
            <p class="footer-stack">Built with Streamlit &middot; TensorFlow Lite &middot; MobileNetV2</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_card(predicted_class: str, confidence: float) -> str:
    """
    Builds the result card HTML (predicted class + confidence bar).
    No JIS-grade field by design -- see module docstring.
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


def render_result_placeholder():

    return """
    <div class="sparkx-result-placeholder">

        <div class="sparkx-result-icon">
            ✦
        </div>

        <div class="sparkx-result-title">
            Ready for analysis
        </div>

        <div class="sparkx-result-description">
            Upload a spark-test image or video
            to identify the material.
        </div>

    </div>
    """