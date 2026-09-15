import streamlit as st


def load_styles():

    st.markdown("""
    <style>

    /* ================================
       GLOBAL
    ================================= */

    .stApp {
        background: #F7FAF7;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ================================
       NAVIGATION
    ================================= */

    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;

        background: rgba(255,255,255,0.95);

        padding: 15px 25px;

        border-radius: 18px;

        border: 1px solid #E4ECE6;

        margin-bottom: 25px;
    }

    .brand {
        font-size: 24px;
        font-weight: 800;
        color: #123D2D;
    }

    .brand span {
        color: #2E9B62;
    }

    /* ================================
       HERO
    ================================= */

    .hero {
        background:
            linear-gradient(
                110deg,
                #E7F5EB 0%,
                #F8FCF9 55%,
                #E3F3E8 100%
            );

        border-radius: 30px;

        padding: 65px 60px;

        border: 1px solid #DCEBE0;

        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 54px;
        line-height: 1.05;
        font-weight: 800;
        color: #123D2D;
        letter-spacing: -2px;
    }

    .hero-title span {
        color: #2E9B62;
    }

    .hero-description {
        font-size: 18px;
        line-height: 1.7;
        color: #63756B;

        max-width: 620px;

        margin-top: 20px;
    }

    /* ================================
       FEATURE CARDS
    ================================= */

    .feature {
        background: white;

        border-radius: 22px;

        padding: 28px;

        border: 1px solid #E3ECE6;

        min-height: 180px;

        box-shadow:
            0 8px 30px rgba(20,70,45,0.05);
    }

    .feature-icon {
        font-size: 36px;
        margin-bottom: 15px;
    }

    .feature-title {
        color: #163F2F;

        font-size: 20px;

        font-weight: 700;

        margin-bottom: 8px;
    }

    .feature-text {
        color: #718078;

        font-size: 14px;

        line-height: 1.6;
    }

    /* ================================
       SECTION
    ================================= */

    .section-title {
        color: #163F2F;

        font-size: 30px;

        font-weight: 800;

        margin-top: 40px;

        margin-bottom: 18px;
    }

    .section-subtitle {
        color: #748078;

        font-size: 15px;

        margin-bottom: 25px;
    }

    /* ================================
       HOW IT WORKS
    ================================= */

    .step {
        background: white;

        border-radius: 20px;

        padding: 25px;

        border: 1px solid #E4ECE7;

        text-align: center;
    }

    .step-number {
        width: 42px;
        height: 42px;

        border-radius: 50%;

        background: #E1F3E7;

        color: #228653;

        display: flex;

        align-items: center;
        justify-content: center;

        margin: 0 auto 15px auto;

        font-weight: 800;
    }

    .step-title {
        color: #173E2E;

        font-weight: 700;

        font-size: 17px;
    }

    .step-text {
        color: #77837C;

        font-size: 13px;

        line-height: 1.5;
    }

    /* ================================
       BUTTONS
    ================================= */

    .stButton > button {

        border-radius: 12px;

        min-height: 45px;

        font-weight: 700;

        border: 1px solid #D8E7DD;
    }

    /* ================================
       FOOTER
    ================================= */

    .footer {
        text-align: center;

        color: #89958E;

        font-size: 13px;

        margin-top: 60px;

        padding-top: 25px;

        border-top: 1px solid #E0E8E3;
    }

    </style>
    """, unsafe_allow_html=True)