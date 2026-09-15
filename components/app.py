import streamlit as st

from components.styles import load_styles


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="PlantCare AI",
    page_icon="🌿",
    layout="wide"
)


# ==========================================
# LOAD DESIGN
# ==========================================

load_styles()


# ==========================================
# TOP NAVIGATION
# ==========================================

st.markdown("""
<div class="top-nav">

    <div class="brand">
        🌿 Plant<span>Care AI</span>
    </div>

    <div style="
        color:#63756B;
        font-size:14px;
    ">
        Smart Plant Health Assistant
    </div>

</div>
""", unsafe_allow_html=True)


# ==========================================
# HERO
# ==========================================

st.markdown("""
<div class="hero">

    <div class="hero-title">

        Smarter Plants.<br>

        <span>Healthier Crops.</span>

    </div>

    <div class="hero-description">

        AI-powered plant disease detection and
        intelligent treatment guidance for
        healthier and stronger plants.

    </div>

</div>
""", unsafe_allow_html=True)


# ==========================================
# ACTION BUTTONS
# ==========================================

col1, col2, col3 = st.columns([1.2, 1.2, 3])

with col1:

    if st.button(
        "🔬 Start Detection",
        use_container_width=True
    ):
        st.info(
            "Disease Detection will be connected next."
        )

with col2:

    if st.button(
        "🌱 Explore Plants",
        use_container_width=True
    ):
        st.info(
            "Plant Explorer will be connected next."
        )


# ==========================================
# FEATURES
# ==========================================

st.markdown(
    '<div class="section-title">Everything your plants need</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'From disease detection to treatment and prevention, '
    'PlantCare AI brings plant health information together.'
    '</div>',
    unsafe_allow_html=True
)


f1, f2, f3 = st.columns(3)


with f1:

    st.markdown("""
    <div class="feature">

        <div class="feature-icon">
            🔬
        </div>

        <div class="feature-title">
            AI Disease Detection
        </div>

        <div class="feature-text">
            Upload a plant leaf image and
            identify possible diseases using
            artificial intelligence.
        </div>

    </div>
    """, unsafe_allow_html=True)


with f2:

    st.markdown("""
    <div class="feature">

        <div class="feature-icon">
            💊
        </div>

        <div class="feature-title">
            Smart Treatment
        </div>

        <div class="feature-text">
            Discover suitable organic and
            chemical treatment information
            for detected diseases.
        </div>

    </div>
    """, unsafe_allow_html=True)


with f3:

    st.markdown("""
    <div class="feature">

        <div class="feature-icon">
            🛡️
        </div>

        <div class="feature-title">
            Disease Prevention
        </div>

        <div class="feature-text">
            Learn practical prevention methods
            to protect plants from future diseases.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ==========================================
# HOW IT WORKS
# ==========================================

st.markdown(
    '<div class="section-title">How PlantCare AI works</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Four simple steps from image to plant health guidance.'
    '</div>',
    unsafe_allow_html=True
)


s1, s2, s3, s4 = st.columns(4)


steps = [
    ("01", "Upload", "Upload a clear image of the affected plant leaf."),
    ("02", "Analyze", "Our AI model analyzes visual characteristics."),
    ("03", "Diagnose", "The system predicts the most likely disease."),
    ("04", "Treat", "Get symptoms, medicines and prevention guidance.")
]


for column, step in zip(
    [s1, s2, s3, s4],
    steps
):

    number, title, description = step

    with column:

        st.markdown(f"""
        <div class="step">

            <div class="step-number">
                {number}
            </div>

            <div class="step-title">
                {title}
            </div>

            <br>

            <div class="step-text">
                {description}
            </div>

        </div>
        """, unsafe_allow_html=True)


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">

    🌿 <b>PlantCare AI</b>

    <br><br>

    AI-powered Plant Disease Detection &
    Remedy System

</div>
""", unsafe_allow_html=True)