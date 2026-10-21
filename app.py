from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_babel import Babel,get_locale

import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from dotenv import load_dotenv
load_dotenv()
import re
import psycopg2
import psycopg2.extensions
import uuid
import cv2
import numpy as np

from PIL import Image

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash


# ==========================================
# MULTILINGUAL SUPPORT
# ==========================================
TRANSLATIONS = {

    "en": {

        # =========================
        # SIDEBAR
        # =========================

        "dashboard": "Dashboard",
        "new_detection": "New Detection",
        "plant_library": "Plant Library",
        "prediction_history": "Prediction History",
        "settings": "Settings",
        "logout": "Logout",

        # =========================
        # DASHBOARD HERO
        # =========================

        "overview": "OVERVIEW",
        "welcome": "Welcome back!",
        "keep_plants_healthy": "Keep your plants healthy with AI-powered care.",
        "ai_powered": "AI-POWERED PLANT DETECTION",
        "plant_feeling_unwell": "Is your plant feeling unwell?",
        "upload_clear_image": "Upload a clear image of your plant leaf and let PlantCare AI identify possible diseases and provide personalized care guidance.",
        "start_new_detection": "Start New Detection",

        # =========================
        # STATISTICS
        # =========================

        "total_predictions": "Total Predictions",
        "plants_analyzed": "Plants Analyzed",
        "healthy_plants": "Healthy Plants",
        "remedies_viewed": "Remedies Viewed",

        "ai_analyses": "AI analyses",
        "plant_varieties": "Plant varieties",
        "healthy_results": "Healthy results",
        "helpful_guidance": "Helpful guidance",

        # =========================
        # ANALYTICS
        # =========================

        "disease_analytics": "DISEASE ANALYTICS",
        "disease_distribution": "Disease Distribution",
        "detected_plant_diseases": "Your detected plant diseases",

        "activity": "ACTIVITY",
        "prediction_activity": "Prediction Activity",
        "your_last_7_days": "Your last 7 days",

        # =========================
        # RECENT PREDICTIONS
        # =========================

        "recent_predictions": "Recent Predictions",
        "view_all": "View All",

        "plant": "Plant",
        "disease": "Disease",
        "confidence": "Confidence",
        "date": "Date",

        # =========================
        # QUICK ACCESS
        # =========================

        "quick_access": "Quick Access",
        "upload_plant_image": "Upload Plant Image",
        "check_plant_health": "Check your plant health",
        "browse_plant_library": "Browse Plant Library",
        "learn_about_plants": "Learn about plants and diseases",
        "view_prediction_history": "View Prediction History",
        "track_previous_predictions": "Track your previous predictions",

        # =========================
        # AI RESULT
        # =========================

        "ai_analysis_complete": "AI ANALYSIS COMPLETE",
        "recommended_remedy": "Recommended Remedy",
        "prevention": "Prevention",
        "chemical_treatment": "Chemical Treatment",

        "no_remedy": "No remedy information available.",
        "no_prevention": "No prevention information available.",
        "no_chemical_treatment": "No chemical treatment information available.",
        
        "quick_access": "QUICK ACCESS",
        "explore_plantcare": "Explore PlantCare",
        "analyze_plant_image": "Analyze a plant image",
        "ai_analysis_complete": "AI ANALYSIS COMPLETE",
        "confidence": "confidence",
        "plant": "Plant",
        "no_remedy": "No remedy information available.",
        "no_prevention": "No prevention information available.",
        "no_chemical": "No chemical treatment information available.",
        "plantcare_tip": "PlantCare Tip",
        "tip_description": "Use clear, well-lit leaf images for better AI detection accuracy. Check your plants regularly to catch diseases early.",
        "predictions": "Predictions",
        "prediction_count": "prediction(s)",
        # =========================
        # BUTTONS
        # =========================

        "start_detection": "Start New Detection",
        "view_history": "View History",
        "choose_image": "Choose Plant Image",
        "detect_disease": "Detect Disease",
        "analysis_completed_description": "PlantCare AI has completed the image analysis and identified the condition shown above.",
        # =========================
        # HELP / TIP
        # =========================
        "need_help": "Need help?",
        "explore_plantcare": "Explore PlantCare AI",
        "plantcare_tip": "PlantCare Tip",
        "tip_text": "Use clear, well-lit leaf images for better AI detection accuracy. Check your plants regularly to catch diseases early.",
                "main_menu": "MAIN MENU",
        "account": "ACCOUNT",
        "my_profile": "My Profile",
        "notifications": "Notifications",
        "recent_activity": "RECENT ACTIVITY",
        "latest_result": "LATEST RESULT",
        "latest_plant_prediction": "Latest Plant Prediction",
        "plant": "Plant",
        "detected_disease": "Detected Disease",
        "confidence": "Confidence",
        "estimated_severity": "Estimated Severity",
        "recommended_remedy": "Recommended Remedy",
        "prevention": "Prevention",
        "chemical_treatment": "Chemical Treatment",
        "severity_disclaimer": "Severity is an experimental colour-based estimate, not a validated diagnosis.",
        "healthy_classifier_message": "The classifier identified this plant as healthy. Disease severity is not applicable.",
        "analyze_another_plant": "Analyze Another Plant",
        "start_new_analysis": "Start a new plant analysis",
        "unavailable": "Unavailable",
        "no_remedy_info": "No remedy information available.",
        "no_prevention_info": "No prevention information available.",
        "no_chemical_info": "No chemical treatment information available.",
        "my_profile": "My Profile",
        "send_message": "Send Message",
        "add_new_plant": "Add New Plant",
        # =========================
        # LANGUAGE
        # =========================

        "english": "English",
        "tamil": "தமிழ்"
    },


    "ta": {

        # =========================
        # SIDEBAR
        # =========================

        "dashboard": "முகப்பு",
        "new_detection": "புதிய கண்டறிதல்",
        "plant_library": "தாவர நூலகம்",
        "prediction_history": "கணிப்பு வரலாறு",
        "settings": "அமைப்புகள்",
        "logout": "வெளியேறு",

        # =========================
        # DASHBOARD HERO
        # =========================

        "overview": "மேலோட்டம்",
        "welcome": "மீண்டும் வரவேற்கிறோம்!",
        "keep_plants_healthy": "AI அடிப்படையிலான பராமரிப்புடன் உங்கள் தாவரங்களை ஆரோக்கியமாக வைத்திருங்கள்.",
        "ai_powered": "AI அடிப்படையிலான தாவர நோய் கண்டறிதல்",
        "plant_feeling_unwell": "உங்கள் தாவரம் பாதிக்கப்பட்டுள்ளதா?",
        "upload_clear_image": "உங்கள் தாவர இலையின் தெளிவான படத்தை பதிவேற்றுங்கள். PlantCare AI சாத்தியமான நோய்களை கண்டறிந்து தனிப்பயனாக்கப்பட்ட பராமரிப்பு வழிகாட்டுதலை வழங்கும்.",
        "start_new_detection": "புதிய கண்டறிதலைத் தொடங்கவும்",

        # =========================
        # STATISTICS
        # =========================

        "total_predictions": "மொத்த கணிப்புகள்",
        "plants_analyzed": "பகுப்பாய்வு செய்யப்பட்ட தாவரங்கள்",
        "healthy_plants": "ஆரோக்கியமான தாவரங்கள்",
        "remedies_viewed": "பார்க்கப்பட்ட தீர்வுகள்",

        "ai_analyses": "AI பகுப்பாய்வுகள்",
        "plant_varieties": "தாவர வகைகள்",
        "healthy_results": "ஆரோக்கியமான முடிவுகள்",
        "helpful_guidance": "பயனுள்ள வழிகாட்டுதல்",

        # =========================
        # ANALYTICS
        # =========================


        "quick_access": "விரைவு அணுகல்",
        "explore_plantcare": "PlantCare ஐ ஆராயுங்கள்",
        "analyze_plant_image": "தாவரப் படத்தை பகுப்பாய்வு செய்யவும்",
        "ai_analysis_complete": "AI பகுப்பாய்வு முடிந்தது",
        "confidence": "நம்பகத்தன்மை",
        "plant": "தாவரம்",
        "no_remedy": "தீர்வு தகவல் எதுவும் இல்லை.",
        "no_prevention": "தடுப்பு தகவல் எதுவும் இல்லை.",
        "no_chemical": "இரசாயன சிகிச்சை தகவல் எதுவும் இல்லை.",
        "plantcare_tip": "PlantCare குறிப்பு",
        "tip_description": "சிறந்த AI கண்டறிதல் துல்லியத்திற்கு தெளிவான மற்றும் நல்ல வெளிச்சம் உள்ள இலைப் படங்களைப் பயன்படுத்தவும். நோய்களை ஆரம்பத்திலேயே கண்டறிய உங்கள் தாவரங்களை தொடர்ந்து பரிசோதிக்கவும்.",
        "predictions": "கணிப்புகள்",
        "prediction_count": "கணிப்பு(கள்)",
        "disease_analytics": "நோய் பகுப்பாய்வு",
        "disease_distribution": "நோய் விநியோகம்",
        "detected_plant_diseases": "கண்டறியப்பட்ட தாவர நோய்கள்",

        "activity": "செயல்பாடு",
        "prediction_activity": "கணிப்பு செயல்பாடு",
        "your_last_7_days": "உங்கள் கடந்த 7 நாட்கள்",

        # =========================
        # RECENT PREDICTIONS
        # =========================

        "recent_predictions": "சமீபத்திய கணிப்புகள்",
        "view_all": "அனைத்தையும் காண்க",

        "plant": "தாவரம்",
        "disease": "நோய்",
        "confidence": "நம்பகத்தன்மை",
        "date": "தேதி",
        "analysis_completed_description": "PlantCare AI படப் பகுப்பாய்வை முடித்து, மேலே காட்டப்பட்டுள்ள நிலையை கண்டறிந்துள்ளது.",
        # =========================
        # QUICK ACCESS
        # =========================

        "quick_access": "விரைவு அணுகல்",
        "upload_plant_image": "தாவரப் படத்தை பதிவேற்றவும்",
        "check_plant_health": "உங்கள் தாவரத்தின் ஆரோக்கியத்தை சரிபார்க்கவும்",
        "browse_plant_library": "தாவர நூலகத்தைப் பார்க்கவும்",
        "learn_about_plants": "தாவரங்கள் மற்றும் நோய்களைப் பற்றி அறியவும்",
        "view_prediction_history": "கணிப்பு வரலாற்றைப் பார்க்கவும்",
        "track_previous_predictions": "முந்தைய கணிப்புகளைப் பார்க்கவும்",

        # =========================
        # AI RESULT
        # =========================

        "ai_analysis_complete": "AI பகுப்பாய்வு முடிந்தது",
        "recommended_remedy": "பரிந்துரைக்கப்படும் தீர்வு",
        "prevention": "தடுப்பு",
        "chemical_treatment": "இரசாயன சிகிச்சை",

        "no_remedy": "தீர்வு தொடர்பான தகவல் இல்லை.",
        "no_prevention": "தடுப்பு தொடர்பான தகவல் இல்லை.",
        "no_chemical_treatment": "இரசாயன சிகிச்சை தொடர்பான தகவல் இல்லை.",

        # =========================
        # BUTTONS
        # =========================

        "start_detection": "புதிய கண்டறிதலைத் தொடங்கவும்",
        "view_history": "வரலாற்றைக் காண்க",
        "choose_image": "தாவரப் படத்தைத் தேர்வு செய்யவும்",
        "detect_disease": "நோயைக் கண்டறியவும்",

        # =========================
        # HELP / TIP
        # =========================

        "need_help": "உதவி தேவையா?",
        "explore_plantcare": "PlantCare AI-ஐ ஆராயுங்கள்",
        "plantcare_tip": "PlantCare குறிப்பு",
        "tip_text": "சிறந்த AI கண்டறிதல் துல்லியத்திற்காக தெளிவான, நல்ல வெளிச்சம் உள்ள தாவர இலைப் படங்களைப் பயன்படுத்தவும். நோய்களை ஆரம்பத்திலேயே கண்டறிய உங்கள் தாவரங்களைத் தொடர்ந்து சரிபார்க்கவும்.",
        "my_profile": "எனது சுயவிவரம்",
        "send_message": "செய்தி அனுப்பு",
        "add_new_plant": "புதிய தாவரத்தைச் சேர்",
        # =========================
        # LANGUAGE
        # =========================

        "english": "English",
        "tamil": "தமிழ்"
    }
}
TAMIL_GUIDE = {

    "Bacterial Spot": {
        "name": "பாக்டீரியா புள்ளி நோய்",
        "description": "தக்காளியில் ஏற்படும் பாக்டீரியா புள்ளி நோய்.",
        "remedy": "பாதிக்கப்பட்ட இலைகளை அகற்றி, தேவையானால் பொருத்தமான பாக்டீரியா எதிர்ப்பு மருந்தைப் பயன்படுத்தவும்.",
        "prevention": "மேலிருந்து நீர் பாய்ச்சுவதைத் தவிர்த்து, நல்ல சுகாதாரத்தைப் பராமரிக்கவும்."
    },

    "Early Blight": {
        "name": "ஆரம்ப கருகல் நோய்",
        "description": "தக்காளியின் இலைகள் மற்றும் பழங்களை பாதிக்கும் பொதுவான பூஞ்சை நோய்.",
        "remedy": "பாதிக்கப்பட்ட இலைகளை அகற்றி, மருந்தின் வழிமுறைகளின்படி பொருத்தமான பூஞ்சைக் கொல்லியைப் பயன்படுத்தவும்.",
        "prevention": "தாவரத்தைச் சுற்றியுள்ள பகுதியை சுத்தமாக வைத்திருந்து, பாதிக்கப்பட்ட தாவரப் பகுதிகளை அகற்றி, இலைகளில் நீர் நீண்ட நேரம் தங்குவதைத் தவிர்க்கவும்."
    },

    "Healthy": {
        "name": "ஆரோக்கியமான தாவரம்",
        "description": "ஆரோக்கியமான தாவரம்.",
        "remedy": "ஆரோக்கியமான தாவரத்திற்கு சிகிச்சை தேவையில்லை.",
        "prevention": "தொடர்ந்து சரியான நீர்ப்பாசனம், ஊட்டச்சத்து மற்றும் தாவர கண்காணிப்பை மேற்கொள்ளவும்."
    },

    "Late Blight": {
        "name": "தாமத கருகல் நோய்",
        "description": "தக்காளியின் இலைகள் மற்றும் பழங்களில் கருமையான புள்ளிகள் அல்லது காயங்களை ஏற்படுத்தும் தீவிர நோய்.",
        "remedy": "பாதிக்கப்பட்ட இலைகளை அகற்றி, பொருத்தமான பூஞ்சைக் கொல்லியைப் பயன்படுத்தவும்.",
        "prevention": "மேலிருந்து நீர் பாய்ச்சுவதைத் தவிர்த்து, நல்ல காற்றோட்டத்தைப் பராமரிக்கவும்."
    },

    "Leaf Mold": {
        "name": "இலை பூஞ்சை நோய்",
        "description": "தக்காளி இலைகளில் மஞ்சள் புள்ளிகள் மற்றும் பூஞ்சை வளர்ச்சியை ஏற்படுத்தும் பூஞ்சை நோய்.",
        "remedy": "பாதிக்கப்பட்ட இலைகளை அகற்றி, நல்ல காற்றோட்டத்தை ஏற்படுத்தவும். பொருத்தமான பூஞ்சைக் கொல்லியைப் பயன்படுத்தவும்.",
        "prevention": "இலைகளை ஈரமாக்குவதைத் தவிர்த்து, பாதிக்கப்பட்ட தாவரக் கழிவுகளை அகற்றவும்."
    },

    "Septoria Leaf Spot": {
        "name": "செப்டோரியா இலைப் புள்ளி நோய்",
        "description": "தக்காளியில் ஏற்படும் செப்டோரியா இலைப் புள்ளி நோய்.",
        "remedy": "பாதிக்கப்பட்ட இலைகளை அகற்றி, பொருத்தமான பூஞ்சைக் கொல்லியைப் பயன்படுத்தவும்.",
        "prevention": "மேலிருந்து நீர் பாய்ச்சுவதைத் தவிர்த்து, பாதிக்கப்பட்ட தாவரக் கழிவுகளை அகற்றவும்."
    },

    "Spider Mites Two Spotted Spider Mite": {
        "name": "இரண்டு புள்ளி சிலந்திப் பூச்சி தாக்குதல்",
        "description": "தக்காளியில் ஏற்படும் சிலந்திப் பூச்சி தாக்குதல்.",
        "remedy": "கடுமையாக பாதிக்கப்பட்ட இலைகளை அகற்றி, பொருத்தமான பூச்சி/மைட் கட்டுப்பாட்டு சிகிச்சையைப் பயன்படுத்தவும்.",
        "prevention": "தாவரங்களை தொடர்ந்து பரிசோதித்து, சிலந்திப் பூச்சிகளுக்கு தங்குமிடமாக இருக்கும் களைகளை கட்டுப்படுத்தவும்."
    },

    "Target Spot": {
        "name": "இலக்கு புள்ளி நோய்",
        "description": "தக்காளியில் ஏற்படும் இலக்கு புள்ளி நோய்.",
        "remedy": "பாதிக்கப்பட்ட இலைகளை அகற்றி, பொருத்தமான பூஞ்சைக் கொல்லியைப் பயன்படுத்தவும்.",
        "prevention": "நல்ல காற்றோட்டத்தைப் பராமரித்து, இலைகளில் நீர் நீண்ட நேரம் தங்குவதைத் தவிர்க்கவும்."
    },

    "Tomato Mosaic Virus": {
        "name": "தக்காளி மொசைக் வைரஸ்",
        "description": "தக்காளியில் ஏற்படும் மொசைக் வைரஸ் நோய்.",
        "remedy": "தேவையான போது பாதிக்கப்பட்ட தாவரங்களை அகற்றி, நோயைப் பரப்பும் பூச்சிகளைக் கட்டுப்படுத்தவும்.",
        "prevention": "ஆரோக்கியமான நடவு பொருட்களைப் பயன்படுத்தி, நோயைப் பரப்பும் பூச்சிகளைக் கட்டுப்படுத்தவும்."
    },

    "Tomato Yellow Leaf Curl Virus": {
        "name": "தக்காளி மஞ்சள் இலை சுருள் வைரஸ்",
        "description": "தக்காளி இலைகளில் மஞ்சள் நிறம் மற்றும் சுருட்டலை ஏற்படுத்தும் வைரஸ் நோய்.",
        "remedy": "கடுமையாக பாதிக்கப்பட்ட தாவரங்களை அகற்றி, நோயைப் பரப்பும் பூச்சிகளைக் கட்டுப்படுத்தவும்.",
        "prevention": "ஆரோக்கியமான தாவரங்களைப் பயன்படுத்தி, வெள்ளை ஈக்களின் எண்ணிக்கையை கட்டுப்படுத்தவும்."
    }
}  
# ============================================================
# ADD THESE KEYS to TRANSLATIONS["en"] and TRANSLATIONS["ta"]
# in app.py (merge into your existing dict, don't replace it)
# ============================================================

# ---------- Add to TRANSLATIONS["en"] ----------
EN_ADDITIONS = {
    # detect.html
    "ai_detection_label": "AI DETECTION",
    "new_plant_detection_title": "New Plant Detection 🔬",
    "new_plant_detection_desc": "Upload a clear leaf image and let PlantCare AI identify possible diseases.",
    "plant_care_member": "Plant Care Member",
    "lets_check_plant": "Let's check your plant",
    "detect_hero_desc": "Upload a clear photo of a plant leaf. Our trained AI model will analyze the image and provide disease information, confidence, remedies and prevention guidance.",
    "upload_format_hint": "JPG, JPEG or PNG • Clear leaf images work best",
    "choose_image_short": "Choose Image",
    "analyze_plant_button": "🔬 Analyze Plant",
    "tip_lighting_title": "☀️ Good Lighting",
    "tip_lighting_desc": "Take the photo in bright, natural light.",
    "tip_leaf_title": "🍃 Clear Leaf",
    "tip_leaf_desc": "Make sure the affected leaf is clearly visible.",
    "tip_quality_title": "📸 Good Quality",
    "tip_quality_desc": "Avoid blurry or very dark images.",

    # login.html
    "welcome_back_healthier": "Welcome back to healthier plants.",
    "smart_plant_health_badge": "🌱 Smart Plant Health",
    "login_subtitle": "Continue your journey with AI-powered plant disease detection, smart remedies, and prevention guidance.",
    "ai_plant_analysis": "AI Plant Analysis",
    "ready_when_you_are": "Ready when you are",
    "sign_in_to_account": "Sign in to your account",
    "enter_details_continue": "Enter your details to continue.",
    "email_address": "Email address",
    "password_label": "Password",
    "forgot_password": "Forgot password?",
    "remember_me": "Remember me",
    "sign_in": "Sign In",
    "or_divider": "or",
    "no_account_yet": "Don't have an account?",
    "create_account_link": "Create an account",

    # history.html
    "review_previous_detections": "Review your previous plant disease detections and AI predictions.",
    "plant_health_journey": "Your Plant Health Journey 🌱",
    "keep_track_desc": "Keep track of your previous AI analyses, confidence scores, and plant disease detections in one place.",
    "average_confidence": "Average Confidence",
    "recent_analyses": "Recent Analyses",
    "latest_predictions_desc": "Your latest plant disease predictions",
    "search_history_placeholder": "Search plant or disease...",
    "prediction_id_label": "Prediction ID",
    "time_label": "Time",
    "ai_confidence_label": "AI Confidence",
    "no_matching_predictions": "No matching predictions",
    "try_other_search": "Try searching for another plant or disease.",
    "history_empty_title": "Your history is empty",
    "history_empty_desc": "Upload your first plant image and let PlantCare AI analyze its health.",
}

# ---------- Add to TRANSLATIONS["ta"] ----------
# NOTE: I've done my best on these Tamil translations, but I'm not
# a certified translator — please have a Tamil speaker review before
# shipping, especially the longer sentences.
TA_ADDITIONS = {
    # detect.html
    "ai_detection_label": "AI கண்டறிதல்",
    "new_plant_detection_title": "புதிய தாவர கண்டறிதல் 🔬",
    "new_plant_detection_desc": "தெளிவான இலைப் படத்தை பதிவேற்றுங்கள், PlantCare AI சாத்தியமான நோய்களை கண்டறியும்.",
    "plant_care_member": "PlantCare உறுப்பினர்",
    "lets_check_plant": "உங்கள் தாவரத்தை சரிபார்ப்போம்",
    "detect_hero_desc": "தாவர இலையின் தெளிவான புகைப்படத்தை பதிவேற்றவும். எங்கள் பயிற்சி பெற்ற AI மாதிரி படத்தை பகுப்பாய்வு செய்து நோய் தகவல், நம்பகத்தன்மை, தீர்வுகள் மற்றும் தடுப்பு வழிகாட்டுதலை வழங்கும்.",
    "upload_format_hint": "JPG, JPEG அல்லது PNG • தெளிவான இலைப் படங்கள் சிறந்தவை",
    "choose_image_short": "படத்தைத் தேர்வு செய்யவும்",
    "analyze_plant_button": "🔬 தாவரத்தை பகுப்பாய்வு செய்யவும்",
    "tip_lighting_title": "☀️ நல்ல வெளிச்சம்",
    "tip_lighting_desc": "பிரகாசமான, இயற்கை வெளிச்சத்தில் புகைப்படம் எடுக்கவும்.",
    "tip_leaf_title": "🍃 தெளிவான இலை",
    "tip_leaf_desc": "பாதிக்கப்பட்ட இலை தெளிவாகத் தெரிகிறதா என்பதை உறுதிசெய்யவும்.",
    "tip_quality_title": "📸 நல்ல தரம்",
    "tip_quality_desc": "மங்கலான அல்லது இருண்ட படங்களைத் தவிர்க்கவும்.",

    # login.html
    "welcome_back_healthier": "ஆரோக்கியமான தாவரங்களுக்கு மீண்டும் வரவேற்கிறோம்.",
    "smart_plant_health_badge": "🌱 ஸ்மார்ட் தாவர ஆரோக்கியம்",
    "login_subtitle": "AI அடிப்படையிலான தாவர நோய் கண்டறிதல், ஸ்மார்ட் தீர்வுகள் மற்றும் தடுப்பு வழிகாட்டுதலுடன் உங்கள் பயணத்தைத் தொடரவும்.",
    "ai_plant_analysis": "AI தாவர பகுப்பாய்வு",
    "ready_when_you_are": "நீங்கள் தயாராக இருக்கும்போது தயார்",
    "sign_in_to_account": "உங்கள் கணக்கில் உள்நுழையவும்",
    "enter_details_continue": "தொடர உங்கள் விவரங்களை உள்ளிடவும்.",
    "email_address": "மின்னஞ்சல் முகவரி",
    "password_label": "கடவுச்சொல்",
    "forgot_password": "கடவுச்சொல் மறந்துவிட்டதா?",
    "remember_me": "என்னை நினைவில் கொள்ளவும்",
    "sign_in": "உள்நுழையவும்",
    "or_divider": "அல்லது",
    "no_account_yet": "கணக்கு இல்லையா?",
    "create_account_link": "கணக்கை உருவாக்கவும்",

    # history.html
    "review_previous_detections": "உங்கள் முந்தைய தாவர நோய் கண்டறிதல்கள் மற்றும் AI கணிப்புகளை பார்வையிடவும்.",
    "plant_health_journey": "உங்கள் தாவர ஆரோக்கிய பயணம் 🌱",
    "keep_track_desc": "உங்கள் முந்தைய AI பகுப்பாய்வுகள், நம்பகத்தன்மை மதிப்பெண்கள் மற்றும் தாவர நோய் கண்டறிதல்களை ஒரே இடத்தில் கண்காணிக்கவும்.",
    "average_confidence": "சராசரி நம்பகத்தன்மை",
    "recent_analyses": "சமீபத்திய பகுப்பாய்வுகள்",
    "latest_predictions_desc": "உங்கள் சமீபத்திய தாவர நோய் கணிப்புகள்",
    "search_history_placeholder": "தாவரம் அல்லது நோயைத் தேடவும்...",
    "prediction_id_label": "கணிப்பு ஐடி",
    "time_label": "நேரம்",
    "ai_confidence_label": "AI நம்பகத்தன்மை",
    "no_matching_predictions": "பொருந்தும் கணிப்புகள் இல்லை",
    "try_other_search": "வேறு தாவரம் அல்லது நோயைத் தேடவும்.",
    "history_empty_title": "உங்கள் வரலாறு காலியாக உள்ளது",
    "history_empty_desc": "உங்கள் முதல் தாவரப் படத்தை பதிவேற்றி PlantCare AI அதன் ஆரோக்கியத்தை பகுப்பாய்வு செய்ய அனுமதிக்கவும்.",
}

# ============================================================
# BATCH 2 — paste these two dicts right after TA_ADDITIONS = {...}
# closes in app.py, THEN add the two .update() lines shown at
# the bottom of this file (do NOT just leave them as a comment
# like last time — they must actually execute).
# ============================================================

EN_ADDITIONS_2 = {
    # register.html
    "create_account_title": "Create Account",
    "start_growing_title": "Start growing healthier crops.",
    "register_subtitle": "Create your PlantCare AI account and get intelligent plant disease detection, remedies and prevention guidance.",
    "ai_plant_protection": "AI Plant Protection",
    "smarter_care_tagline": "Your plants, smarter care.",
    "get_started_label": "GET STARTED",
    "create_your_account": "Create your account",
    "join_plantcare_protect": "Join PlantCare AI and protect your plants.",
    "full_name_label": "Full name",
    "enter_full_name_placeholder": "Enter your full name",
    "create_password_placeholder": "Create a password",
    "confirm_password_label": "Confirm password",
    "confirm_password_placeholder": "Confirm your password",
    "agree_terms": "I agree to the",
    "terms_conditions": "Terms & Conditions",
    "create_account_button": "Create Account",
    "already_have_account": "Already have an account?",

    # plant_library.html
    "back_to_dashboard": "← Dashboard",
    "plant_knowledge_center_label": "🌱 PLANT KNOWLEDGE CENTER",
    "plant_library_hero_desc": "Discover the plants supported by our disease detection system. Explore each plant using its English, Tamil and scientific name.",
    "plants_stat_label": "Plants",
    "name_types_stat_label": "Name Types",
    "supported_plants_heading": "Supported Plants",
    "browse_collection_desc": "Browse our complete collection of supported plants",
    "search_by_plant_name_placeholder": "Search by plant name...",
    "scientific_name_label": "Scientific Name",
    "plant_id_label": "Plant ID",
    "supported_label": "Supported",
    "no_plants_found": "No plants found",
    "try_search_english_tamil": "Try searching using an English, Tamil or scientific name.",

    # admin_dashboard.html
    "admin_dashboard_title": "🌱 PlantCare AI Admin Dashboard",
    "welcome_administrator": "Welcome, Administrator.",
    "registered_users": "Registered Users",
    "id_label": "ID",
    "email_label": "Email",
    "role_label": "Role",
    "created_at_label": "Created At",
    "admin_role_label": "ADMIN",
    "user_role_label": "USER",
}

TA_ADDITIONS_2 = {
    # register.html
    "create_account_title": "கணக்கை உருவாக்கவும்",
    "start_growing_title": "ஆரோக்கியமான பயிர்களை வளர்க்கத் தொடங்குங்கள்.",
    "register_subtitle": "உங்கள் PlantCare AI கணக்கை உருவாக்கி, அறிவார்ந்த தாவர நோய் கண்டறிதல், தீர்வுகள் மற்றும் தடுப்பு வழிகாட்டுதலைப் பெறுங்கள்.",
    "ai_plant_protection": "AI தாவர பாதுகாப்பு",
    "smarter_care_tagline": "உங்கள் தாவரங்கள், சிறந்த பராமரிப்பு.",
    "get_started_label": "தொடங்குங்கள்",
    "create_your_account": "உங்கள் கணக்கை உருவாக்கவும்",
    "join_plantcare_protect": "PlantCare AI-இல் சேர்ந்து உங்கள் தாவரங்களைப் பாதுகாக்கவும்.",
    "full_name_label": "முழு பெயர்",
    "enter_full_name_placeholder": "உங்கள் முழு பெயரை உள்ளிடவும்",
    "create_password_placeholder": "கடவுச்சொல்லை உருவாக்கவும்",
    "confirm_password_label": "கடவுச்சொல்லை உறுதிப்படுத்தவும்",
    "confirm_password_placeholder": "உங்கள் கடவுச்சொல்லை உறுதிப்படுத்தவும்",
    "agree_terms": "நான் ஒப்புக்கொள்கிறேன்",
    "terms_conditions": "விதிமுறைகள் & நிபந்தனைகள்",
    "create_account_button": "கணக்கை உருவாக்கவும்",
    "already_have_account": "ஏற்கனவே கணக்கு உள்ளதா?",

    # plant_library.html
    "back_to_dashboard": "← முகப்பு",
    "plant_knowledge_center_label": "🌱 தாவர அறிவு மையம்",
    "plant_library_hero_desc": "எங்கள் நோய் கண்டறிதல் அமைப்பு ஆதரிக்கும் தாவரங்களைக் கண்டறியவும். ஒவ்வொரு தாவரத்தையும் அதன் ஆங்கிலம், தமிழ் மற்றும் அறிவியல் பெயரைப் பயன்படுத்தி ஆராயுங்கள்.",
    "plants_stat_label": "தாவரங்கள்",
    "name_types_stat_label": "பெயர் வகைகள்",
    "supported_plants_heading": "ஆதரிக்கப்படும் தாவரங்கள்",
    "browse_collection_desc": "ஆதரிக்கப்படும் தாவரங்களின் முழு தொகுப்பையும் பார்வையிடவும்",
    "search_by_plant_name_placeholder": "தாவரத்தின் பெயரால் தேடவும்...",
    "scientific_name_label": "அறிவியல் பெயர்",
    "plant_id_label": "தாவர ஐடி",
    "supported_label": "ஆதரிக்கப்படுகிறது",
    "no_plants_found": "தாவரங்கள் எதுவும் கிடைக்கவில்லை",
    "try_search_english_tamil": "ஆங்கிலம், தமிழ் அல்லது அறிவியல் பெயரைப் பயன்படுத்தி தேடவும்.",

    # admin_dashboard.html
    "admin_dashboard_title": "🌱 PlantCare AI நிர்வாக டாஷ்போர்டு",
    "welcome_administrator": "வரவேற்கிறோம், நிர்வாகி.",
    "registered_users": "பதிவு செய்யப்பட்ட பயனர்கள்",
    "id_label": "ஐடி",
    "email_label": "மின்னஞ்சல்",
    "role_label": "பங்கு",
    "created_at_label": "உருவாக்கப்பட்ட தேதி",
    "admin_role_label": "நிர்வாகி",
    "user_role_label": "பயனர்",
}
# ============================================================
# BATCH 3 — paste right after TA_ADDITIONS_2 = {...} closes,
# then add the two .update() lines at the bottom (not commented
# out — copy exactly as shown, same as batch 2).
# ============================================================

EN_ADDITIONS_3 = {
    "dashboard_description": "Here's what's happening with your plants today.",
    "model_accuracy": "Model Accuracy",
    "analysis_completed": "Analysis Completed",
    "healthy": "Healthy",
    "needs_attention": "Needs Attention",
    "recent": "Recent",
    "no_predictions": "No predictions yet",
    "start_first_detection": "Upload your first plant image to get started.",
    "analyzed_plant": "Analyzed plant",
    "disease_unknown": "Unknown Condition",
}

TA_ADDITIONS_3 = {
    "dashboard_description": "இன்று உங்கள் தாவரங்களில் என்ன நடக்கிறது என்பது இதோ.",
    "model_accuracy": "மாதிரி துல்லியம்",
    "analysis_completed": "பகுப்பாய்வு முடிந்தது",
    "healthy": "ஆரோக்கியமானது",
    "needs_attention": "கவனம் தேவை",
    "recent": "சமீபத்திய",
    "no_predictions": "இதுவரை கணிப்புகள் இல்லை",
    "start_first_detection": "தொடங்க உங்கள் முதல் தாவரப் படத்தை பதிவேற்றவும்.",
    "analyzed_plant": "பகுப்பாய்வு செய்யப்பட்ட தாவரம்",
    "disease_unknown": "அறியப்படாத நிலை",
}

# ============================================================
# THESE MUST ACTUALLY RUN — not commented out:
# ============================================================
TRANSLATIONS["en"].update(EN_ADDITIONS_3)
TRANSLATIONS["ta"].update(TA_ADDITIONS_3)
# ============================================================
# THESE TWO LINES MUST ACTUALLY RUN when pasted into app.py —
# this is the exact step that got skipped last time with
# EN_ADDITIONS/TA_ADDITIONS. They are NOT commented out here
# on purpose — copy them exactly as-is.
# ============================================================
TRANSLATIONS["en"].update(EN_ADDITIONS_2)
TRANSLATIONS["ta"].update(TA_ADDITIONS_2)
TRANSLATIONS["en"].update(EN_ADDITIONS)
TRANSLATIONS["ta"].update(TA_ADDITIONS)

# ============================================================
# LOAD TRAINED PLANT DISEASE MODEL
# ============================================================

MODEL_PATH = "plant_disease_model.tflite"
CLASS_NAMES_PATH = "class_names.txt"
import threading
from ai_edge_litert.interpreter import Interpreter

interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
_inp = interpreter.get_input_details()[0]
_out = interpreter.get_output_details()[0]
_lock = threading.Lock()

def run_model(x):
    with _lock:
        interpreter.set_tensor(_inp["index"], x.astype("float32"))
        interpreter.invoke()
        return interpreter.get_tensor(_out["index"]).copy()
print("Model output shape:",_out["shape"])
with open(CLASS_NAMES_PATH, "r") as f:
    class_names = [line.strip() for line in f.readlines()]

print("ML model loaded successfully!")
print("Number of classes:", len(class_names))


# ============================================================
# FLASK CONFIGURATION
# ============================================================

app = Flask(__name__)
app.config["PROFILE_UPLOAD_FOLDER"] = os.path.join(
    app.root_path, "static", "profile_photos"
)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

os.makedirs(app.config["PROFILE_UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_PROFILE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

def allowed_profile_image(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_PROFILE_EXTENSIONS
    )
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")
if os.getenv("IS_HOSTED"):
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["BABEL_SUPPORTED_LOCALES"] = ["en", "ta"]

def get_user_locale():
    return session.get("language", "en")
@app.route("/notifications")
def notifications():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                notification_id,
                title,
                message,
                type,
                is_read,
                created_at
            FROM NOTIFICATIONS
            WHERE user_id = :user_id
            ORDER BY created_at DESC
        """, {
            "user_id": session["user_id"]
        })

        notification_list = cursor.fetchall()

        return render_template(
            "notifications.html",
            notifications=notification_list
        )

    except psycopg2.Error as error:
        print("Notification Error:", error)
        return redirect(url_for("dashboard"))

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
@app.route("/notifications/mark-read/<int:notification_id>", methods=["POST"])
def mark_notification_read(notification_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE NOTIFICATIONS
            SET IS_READ = 1,
                READ_AT = SYSTIMESTAMP
            WHERE NOTIFICATION_ID = :notification_id
            AND USER_ID = :user_id
            """,
            {
                "notification_id": notification_id,
                "user_id": session["user_id"]
            }
        )

        connection.commit()

        return redirect(
            url_for("notifications")
        )

    except psycopg2.Error as error:

        print(
            "Mark Notification Read Error:",
            error
        )

        if connection:
            connection.rollback()

        return redirect(
            url_for("notifications")
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/notifications/mark-all-read", methods=["POST"])
def mark_all_notifications_read():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE NOTIFICATIONS
            SET IS_READ = 1,
                READ_AT = SYSTIMESTAMP
            WHERE USER_ID = :user_id
            AND IS_READ = 0
            """,
            {
                "user_id": session["user_id"]
            }
        )

        connection.commit()

        return redirect(
            url_for("notifications")
        )

    except psycopg2.Error as error:

        print(
            "Mark All Notifications Read Error:",
            error
        )

        if connection:
            connection.rollback()

        return redirect(
            url_for("notifications")
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

babel = Babel(
    app,
    locale_selector=get_user_locale
)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print("Database URL loaded:", bool(DATABASE_URL))

# ==========================================
# LANGUAGE SWITCH
# ==========================================

@app.route("/set-language/<language>")
def set_language(language):

    if language not in ["en", "ta"]:
        language = "en"

    session["language"] = language

    return redirect(
        request.referrer or url_for("dashboard")
    )
@app.context_processor
def inject_language():

    language = session.get("language", "en")

    return {
        "lang": TRANSLATIONS.get(
            language,
            TRANSLATIONS["en"]
        ),
        "current_language": language
    }


# ============================================================
# POSTGRESQL DATABASE CONNECTION (Neon)
# Oracle-style SQL in this file is auto-translated by PGCursor
# ============================================================

# NUMERIC -> float (Oracle returned floats; keeps templates working)
_DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    "DEC2FLOAT",
    lambda value, cur: float(value) if value is not None else None
)
psycopg2.extensions.register_type(_DEC2FLOAT)


def _oracle_to_pg(sql, has_params):
    sql = re.sub(r"\bNVL\s*\(", "COALESCE(", sql, flags=re.I)
    sql = re.sub(r"\bSYSTIMESTAMP\b", "NOW()", sql, flags=re.I)
    sql = re.sub(r"\bSYSDATE\b", "NOW()", sql, flags=re.I)
    sql = re.sub(r"NOTIFICATIONS_SEQ\.NEXTVAL", "nextval('notifications_seq')", sql, flags=re.I)
    sql = re.sub(
        r"FETCH\s+FIRST\s+(\d+)\s+ROWS?\s+ONLY",
        r"LIMIT \1", sql, flags=re.I
    )
    if has_params:
        sql = sql.replace("%", "%%")
        sql = re.sub(r"(?<![:\w]):([A-Za-z_]\w*)", r"%(\1)s", sql)
    return sql


class PGCursor(psycopg2.extensions.cursor):
    def execute(self, sql, vars=None):
        return super().execute(_oracle_to_pg(sql, vars is not None), vars)


import time

def get_db_connection():
    last_error = None

    for attempt in range(3):
        try:
            conn = psycopg2.connect(
                DATABASE_URL,
                cursor_factory=PGCursor,
                connect_timeout=15,
                keepalives=1,
                keepalives_idle=30,
                keepalives_interval=10,
                keepalives_count=5
            )
            with conn.cursor() as cur:
                cur.execute("SET TIME ZONE 'Asia/Kolkata'")
            conn.commit()
            return conn
        except psycopg2.OperationalError as error:
            last_error = error
            print(f"DB connect attempt {attempt + 1} failed:", error)
            time.sleep(2)

    raise last_error


def add_notification(
    cursor,
    user_id,
    title,
    message,
    notification_type="info",
    sender_id=None,
    link_url=None
):
    cursor.execute("""
        INSERT INTO NOTIFICATIONS (
            NOTIFICATION_ID,
            USER_ID,
            SENDER_ID,
            TITLE,
            MESSAGE,
            TYPE,
            IS_READ,
            CREATED_AT,
            LINK_URL
        )
        VALUES (
            NOTIFICATIONS_SEQ.NEXTVAL,
            :user_id,
            :sender_id,
            :title,
            :message,
            :notification_type,
            0,
            SYSTIMESTAMP,
            :link_url
        )
    """, {
        "user_id": user_id,
        "sender_id": sender_id,
        "title": title,
        "message": message,
        "notification_type": notification_type,
        "link_url": link_url
    })
def notify_all_admins(
    cursor,
    title,
    message,
    notification_type="info",
    sender_id=None,
    link_url=None
):
    cursor.execute("""
        SELECT USER_ID
        FROM USERS
        WHERE UPPER(ROLE) = 'ADMIN'
    """)

    admins = cursor.fetchall()

    for admin in admins:
        admin_id = admin[0]

        add_notification(
            cursor=cursor,
            user_id=admin_id,
            title=title,
            message=message,
            notification_type=notification_type,
            sender_id=sender_id,
            link_url=link_url
        )
def estimate_severity(image_path):
    """
    Experimental visual estimate only.
    Yellow/brown pixels are a proxy for possible damage,
    not a validated plant-disease severity diagnosis.
    """
    image = cv2.imread(image_path)

    if image is None:
        return {
            "severity": "Unable to estimate",
            "affected_percentage": None,
            "note": "Image could not be analyzed."
        }

    # Resize while preserving the image proportions
    h0, w0 = image.shape[:2]
    scale = min(600 / max(h0, w0), 1.0)

    new_w = max(1, int(w0 * scale))
    new_h = max(1, int(h0 * scale))
    image = cv2.resize(image, (new_w, new_h))

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Approximate green pixels to locate the leaf
    green_mask = cv2.inRange(
        hsv,
        np.array([25, 25, 20]),
        np.array([100, 255, 255])
    )

    contours, _ = cv2.findContours(
        green_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return {
            "severity": "Unable to estimate",
            "affected_percentage": None,
            "note": "A clear leaf region could not be identified."
        }

    largest = max(contours, key=cv2.contourArea)

    image_area = image.shape[0] * image.shape[1]

    if cv2.contourArea(largest) < image_area * 0.02:
        return {
            "severity": "Unable to estimate",
            "affected_percentage": None,
            "note": "The leaf region is too small or unclear."
        }

    # Approximate bounding box around the largest green region
    x, y, w, h = cv2.boundingRect(largest)

    pad = int(0.08 * max(w, h))

    x1 = max(0, x - pad)
    y1 = max(0, y - pad)
    x2 = min(image.shape[1], x + w + pad)
    y2 = min(image.shape[0], y + h + pad)

    crop = image[y1:y2, x1:x2].copy()

    if crop.shape[0] < 3 or crop.shape[1] < 3:
        return {
            "severity": "Unable to estimate",
            "affected_percentage": None,
            "note": "The estimated leaf region is too small."
        }

    # Refine approximate leaf/background segmentation
    mask = np.zeros(crop.shape[:2], np.uint8)
    bg_model = np.zeros((1, 65), np.float64)
    fg_model = np.zeros((1, 65), np.float64)

    rect = (
        1,
        1,
        crop.shape[1] - 2,
        crop.shape[0] - 2
    )

    try:
        cv2.grabCut(
            crop,
            mask,
            rect,
            bg_model,
            fg_model,
            5,
            cv2.GC_INIT_WITH_RECT
        )
    except cv2.error:
        return {
            "severity": "Unable to estimate",
            "affected_percentage": None,
            "note": "Leaf segmentation failed; try a clearer image."
        }

    leaf_mask = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD),
        255,
        0
    ).astype(np.uint8)

    leaf_pixels = cv2.countNonZero(leaf_mask)

    if leaf_pixels < 100:
        return {
            "severity": "Unable to estimate",
            "affected_percentage": None,
            "note": "Leaf segmentation was not reliable."
        }

    crop_hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    # Approximate yellow regions
    yellow_mask = cv2.inRange(
        crop_hsv,
        np.array([15, 35, 35]),
        np.array([38, 255, 255])
    )

    # Approximate brown regions
    brown_mask = cv2.inRange(
        crop_hsv,
        np.array([5, 40, 20]),
        np.array([25, 255, 180])
    )

    possible_damage = cv2.bitwise_or(
        yellow_mask,
        brown_mask
    )

    # Reduce small isolated colour noise
    kernel = np.ones((3, 3), np.uint8)

    possible_damage = cv2.morphologyEx(
        possible_damage,
        cv2.MORPH_OPEN,
        kernel
    )

    # Count possible yellow/brown pixels inside the leaf mask
    damage_inside_leaf = cv2.bitwise_and(
        possible_damage,
        possible_damage,
        mask=leaf_mask
    )

    damage_pixels = cv2.countNonZero(damage_inside_leaf)

    percentage = min(
        100.0,
        (damage_pixels / leaf_pixels) * 100
    )

    # Provisional thresholds; validate against labelled images
    if percentage < 10:
        severity = "MILD"
    elif percentage < 25:
        severity = "MODERATE"
    else:
        severity = "SEVERE"

    return {
        "severity": severity,
        "affected_percentage": round(percentage, 1),
        "note": (
            "Experimental estimate of yellow/brown area within the "
            "segmented leaf. Natural coloration, lighting and shadows "
            "may affect results; this is not a validated diagnosis."
        )
    }
# ============================================================
# ML PREDICTION FUNCTION
# ============================================================

def predict_disease(image_path):

    image = Image.open(image_path).convert("RGB")

    image = image.resize((224, 224))

    image_array = np.array(image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    prediction = run_model(image_array)

    predicted_index = np.argmax(prediction[0])

    confidence = float(
        prediction[0][predicted_index]
    ) * 100

    predicted_class = class_names[predicted_index]

    return predicted_class, confidence


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("home.html")


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        connection = None
        cursor = None

        try:

            connection = get_db_connection()

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT user_id, full_name, password_hash, role
                FROM USERS
                WHERE email = :email
                """,
                {"email": email}
            )

            user = cursor.fetchone()

            if user:

                user_id = user[0]
                full_name = user[1]
                password_hash = user[2]
                role = user[3]

                if check_password_hash(password_hash, password):

                    # -----------------------------------------
                    # SAVE USER SESSION
                    # -----------------------------------------

                    session["user_id"] = user_id
                    session["full_name"] = full_name
                    session["email"] = email
                    session["role"] = role

                    # -----------------------------------------
                    # NOTIFY ADMINS ABOUT USER LOGIN
                    # -----------------------------------------

                    if role != "ADMIN":

                        notify_all_admins(
                            cursor=cursor,
                            title="User Login",
                            message=(
                                f"{full_name} logged into "
                                f"PlantCare AI."
                            ),
                            notification_type="login",
                            sender_id=user_id
                        )

                        connection.commit()

                    # -----------------------------------------
                    # ADMIN LOGIN
                    # -----------------------------------------

                    if role == "ADMIN":

                        return redirect(
                            url_for("admin_dashboard")
                        )

                    # -----------------------------------------
                    # NORMAL USER LOGIN
                    # -----------------------------------------

                    else:

                        return redirect(
                            url_for("home")
                        )

            flash("Invalid email or password.")

            return redirect(
                url_for("login")
            )

        except psycopg2.Error as error:

            print("Database Error:", error)

            if connection:
                connection.rollback()

            flash(
                "Unable to connect to the database."
            )

            return redirect(
                url_for("login")
            )

        except Exception as error:

            print("Login Notification Error:", error)

            if connection:
                connection.rollback()

            flash(
                "Unable to complete login."
            )

            return redirect(
                url_for("login")
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("login.html")
# ============================================================
# REGISTER
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get(
            "name", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get(
            "password", ""
        )

        confirm_password = request.form.get(
            "confirm_password", ""
        )

        if not full_name or not email or not password:
            return "Please fill all fields."

        if password != confirm_password:
            return "Passwords do not match."

        password_hash = generate_password_hash(
            password
        )

        connection = None
        cursor = None

        try:

            print("Connecting to database...")

            connection = get_db_connection()

            print("Database connected!")

            cursor = connection.cursor()

            # -------------------------------------------------
            # 1. CREATE NEW USER
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO USERS
                    (full_name, email, password_hash)
                VALUES
                    (:full_name, :email, :password_hash)
                """,
                {
                    "full_name": full_name,
                    "email": email,
                    "password_hash": password_hash
                }
            )

            # -------------------------------------------------
            # 2. GET NEW USER ID
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT USER_ID
                FROM USERS
                WHERE EMAIL = :email
                """,
                {
                    "email": email
                }
            )

            new_user = cursor.fetchone()

            if new_user:

                new_user_id = new_user[0]

                # -------------------------------------------------
                # 3. NOTIFY ALL ADMINS
                # -------------------------------------------------

                notify_all_admins(
                    cursor=cursor,
                    title="New User Registered",
                    message=(
                        f"{full_name} has created a new "
                        f"PlantCare AI account."
                    ),
                    notification_type="registration",
                    sender_id=new_user_id
                )

            # -------------------------------------------------
            # 4. SAVE USER + NOTIFICATION
            # -------------------------------------------------

            connection.commit()

            print("USER INSERTED SUCCESSFULLY!")

            print(
                "ADMIN REGISTRATION NOTIFICATION CREATED!"
            )

            return redirect(
                url_for("login")
            )

        except psycopg2.Error as error:

            print("DATABASE ERROR:", error)

            if connection:
                connection.rollback()

            return f"database error: {error}"

        except Exception as error:

            print("REGISTRATION ERROR:", error)

            if connection:
                connection.rollback()

            return f"Registration error: {error}"

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    return render_template("register.html")
# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        user_id = session["user_id"]
                # ==========================================
        # UNREAD NOTIFICATION COUNT
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM NOTIFICATIONS
            WHERE user_id = :user_id
            AND is_read = 0
        """, {
            "user_id": user_id
        })

        unread_notifications = cursor.fetchone()[0] or 0

        # ==========================================
        # 1. TOTAL PREDICTIONS
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM PREDICTION_HISTORY
            WHERE user_id = :user_id
        """, {
            "user_id": user_id
        })

        total_predictions = cursor.fetchone()[0] or 0
        print("====================================")
        print("DASHBOARD USER ID:", user_id)
        print("TOTAL PREDICTIONS:", total_predictions)
        print("====================================")
        
                # ==========================================
        # CHART DATA
        # ==========================================

        # ------------------------------------------
        # Disease Distribution
        # ------------------------------------------

        cursor.execute("""
            SELECT disease_name, COUNT(*)
            FROM PREDICTION_HISTORY
            WHERE user_id = :user_id
            GROUP BY disease_name
            ORDER BY COUNT(*) DESC
        """, {
            "user_id": user_id
        })

        disease_rows = cursor.fetchall()

        disease_labels = [
            row[0] for row in disease_rows
        ]

        disease_counts = [
            row[1] for row in disease_rows
        ]

        # ------------------------------------------
# Prediction Activity - Last 7 Days
# ------------------------------------------

        cursor.execute("""
        SELECT (CURRENT_DATE - g) AS prediction_date
        FROM generate_series(6, 0, -1) AS g
        ORDER BY prediction_date""")

        date_rows = cursor.fetchall()

# Get prediction counts for the last 7 days
        cursor.execute("""
        SELECT
        CAST(predicted_at AS DATE) AS prediction_date,
        COUNT(*) AS prediction_count
        FROM PREDICTION_HISTORY
        WHERE user_id = :user_id
        AND predicted_at >= CURRENT_DATE - 6
        AND predicted_at < CURRENT_DATE + 1
        GROUP BY CAST(predicted_at AS DATE)
        """, {
        "user_id": user_id
        })
        count_rows = cursor.fetchall()

# Store database counts using the date as the key
        prediction_counts = {
            row[0]: row[1]
            for row in count_rows
        }

# Create all 7 dates, including dates with 0 predictions
        activity_labels = []
        activity_counts = []

        for row in date_rows:
            prediction_date = row[0]

            activity_labels.append(
            prediction_date.strftime("%d %b")
            )

            activity_counts.append(
            prediction_counts.get(prediction_date, 0)
            )
        # ==========================================
        # 2. PLANTS ANALYZED
        # ==========================================

        cursor.execute("""
            SELECT COUNT(DISTINCT plant_name)
            FROM PREDICTION_HISTORY
            WHERE user_id = :user_id
        """, {
            "user_id": user_id
        })

        plants_analyzed = cursor.fetchone()[0] or 0


        # ==========================================
        # 3. HEALTHY PLANTS
        # ==========================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM PREDICTION_HISTORY
            WHERE user_id = :user_id
            AND LOWER(TRIM(disease_name)) = 'healthy'
        """, {
            "user_id": user_id
        })

        healthy_plants = cursor.fetchone()[0] or 0


                # ==========================================
        # RECENT PREDICTIONS
        # ==========================================

        cursor.execute("""
    SELECT
        ph.plant_name,
        ph.disease_name,
        ph.confidence,
        ph.image_path,
        ph.predicted_at,
        r.remedy,
        r.prevention,
        r.chemical_remedy
    FROM prediction_history ph
    LEFT JOIN PLANTS p
    ON LOWER(TRIM(ph.plant_name))
    = LOWER(TRIM(p.plant_name))

    LEFT JOIN DISEASES d
    ON d.plant_id = p.plant_id
    AND LOWER(TRIM(ph.disease_name))
    = LOWER(TRIM(d.disease_name))

        LEFT JOIN REMEDIES r
    ON r.remedy_id = (
        SELECT r2.remedy_id
        FROM REMEDIES r2
        WHERE r2.disease_id = d.disease_id
        AND (
            UPPER(TRIM(r2.severity_level)) =
                UPPER(TRIM(ph.severity_level))
            OR r2.severity_level IS NULL
        )
        ORDER BY
            CASE
                WHEN UPPER(TRIM(r2.severity_level)) =
                    UPPER(TRIM(ph.severity_level))
                THEN 0
                ELSE 1
            END,
            r2.remedy_id
        FETCH FIRST 1 ROW ONLY
    )
    WHERE ph.user_id = :user_id
    ORDER BY ph.predicted_at DESC
    FETCH FIRST 6 ROWS ONLY
    """, {
    "user_id": user_id
    })
        rows = cursor.fetchall()

        recent_predictions = []

        for row in rows:
            recent_predictions.append({
                "plant_name": row[0],
                "disease_name": row[1],
                "confidence": row[2],
                "image_path": row[3],
                "prediction_date": row[4],
                "remedy": row[5],
                "prevention": row[6],
                "chemical_remedy": row[7]
            })
        
        # ==========================================
# LATEST PREDICTION
# ==========================================

        latest_prediction = None

        cursor.execute("""
        SELECT
        ph.plant_name,
        ph.disease_name,
        ph.confidence,
        ph.image_path,
        ph.predicted_at,
        d.description,
        ph.severity_level,
        r.remedy,
        r.prevention,
        r.chemical_remedy
        FROM PREDICTION_HISTORY ph

        LEFT JOIN PLANTS p
        ON LOWER(TRIM(ph.plant_name))
         = LOWER(TRIM(p.plant_name))

        LEFT JOIN DISEASES d
        ON d.plant_id = p.plant_id
        AND LOWER(TRIM(ph.disease_name))
        = LOWER(TRIM(d.disease_name))

                LEFT JOIN REMEDIES r
        ON r.remedy_id = (
            SELECT r2.remedy_id
            FROM REMEDIES r2
            WHERE r2.disease_id = d.disease_id
            AND (
                UPPER(TRIM(r2.severity_level)) =
                    UPPER(TRIM(ph.severity_level))
                OR r2.severity_level IS NULL
            )
            ORDER BY
                CASE
                    WHEN UPPER(TRIM(r2.severity_level)) =
                        UPPER(TRIM(ph.severity_level))
                    THEN 0
                    ELSE 1
                END,
                r2.remedy_id
            FETCH FIRST 1 ROW ONLY
        )

        WHERE ph.user_id = :user_id

        ORDER BY ph.predicted_at DESC

        FETCH FIRST 1 ROW ONLY
        """, {
            "user_id": user_id
        })

        latest_row = cursor.fetchone()

        if latest_row:

            latest_prediction = {
            "plant_name": latest_row[0],
            "disease_name": latest_row[1],
            "confidence": latest_row[2],
            "image_path": latest_row[3],
            "prediction_date": latest_row[4],
            "description": latest_row[5],
            "severity": latest_row[6],
            "remedy": latest_row[7],
            "prevention": latest_row[8],
            "chemical_remedy": latest_row[9]
            }

        print("====================================")
        print("LATEST PREDICTION:", latest_prediction)
        print("====================================")
        # ==========================================
        # DEBUG
        # ==========================================

        print("====================================")
        print("DASHBOARD USER ID:", user_id)
        print("TOTAL PREDICTIONS:", total_predictions)
        print("PLANTS ANALYZED:", plants_analyzed)
        print("HEALTHY PLANTS:", healthy_plants)
        print("RECENT PREDICTIONS:", len(recent_predictions))
        print("====================================")


        return render_template(
        "dashboard.html",

    total_predictions=total_predictions,

    plants_analyzed=plants_analyzed,

    healthy_plants=healthy_plants,
    unread_notifications=unread_notifications,

    recent_predictions=recent_predictions,
    latest_prediction=latest_prediction,

    disease_labels=disease_labels,

    disease_counts=disease_counts,

    activity_labels=activity_labels,

    activity_counts=activity_counts
)
    except psycopg2.Error as error:

        print("Dashboard Error:", error)

        flash("Unable to load dashboard.")

        return redirect(url_for("login"))


    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()
# ============================================================
# ML IMAGE PREDICTION
# ============================================================
@app.route("/detect", methods=["GET"])
def detect():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("detect.html")

@app.route("/predict", methods=["POST"])
def predict():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if "image" not in request.files:
        flash("Please select an image.")
        return redirect(url_for("dashboard"))

    image = request.files["image"]

    if image.filename == "":
        flash("Please select an image.")
        return redirect(url_for("dashboard"))

    upload_folder = "static/uploads"
    os.makedirs(upload_folder, exist_ok=True)

    import uuid

    filename = str(uuid.uuid4()) + "_" + image.filename
    image_path = os.path.join(upload_folder, filename)

    image.save(image_path)

    connection = None
    cursor = None

    try:

        # ==========================================
        # STEP 1: ML PREDICTION
        # ==========================================

        predicted_class, confidence = predict_disease(image_path)

# Clean the predicted class name before checking its status
        if "___" in predicted_class:
            plant_name, disease_name = predicted_class.split("___", 1)
        else:
            plant_name = predicted_class
            disease_name = predicted_class

        disease_check = disease_name.strip().lower().replace("_", " ")

        if disease_check == "healthy":
            severity_result = {
                "severity": "Not Applicable — Healthy Plant",
                "affected_percentage": None,
                "note": "No disease was detected by the classifier. This does not guarantee the plant is disease-free."
            }
        else:
            severity_result = estimate_severity(image_path)

        print("Predicted disease:", predicted_class)
        print("Confidence:", confidence)
        print("Estimated severity:", severity_result["severity"])
        print(
            "Estimated non-green area:",
            severity_result["affected_percentage"]
        )

        CONFIDENCE_THRESHOLD = 70

        low_confidence = confidence < CONFIDENCE_THRESHOLD

        if low_confidence:
            print(
                f"LOW CONFIDENCE: {confidence:.2f}%. "
                "Showing prediction with a warning."
            )
        # ==========================================
        # STEP 2: SPLIT ML CLASS
        # ==========================================

        if "___" in predicted_class:

            plant_name, disease_name = predicted_class.split(
                "___", 1
            )

        else:

            plant_name = predicted_class
            disease_name = predicted_class

        # ==========================================
        # CLEAN PLANT NAME
        # ==========================================

        plant_name = plant_name.replace(
            "_(including_sour)", ""
        )

        plant_name = plant_name.replace(
            "_(maize)", ""
        )

        plant_name = plant_name.replace(
            ",_bell", ""
        )

        # ==========================================
        # CLEAN DISEASE NAME
        # ==========================================

        disease_name = disease_name.replace(
            "_", " "
        )

        disease_name = disease_name.replace(
            "(", ""
        )

        disease_name = disease_name.replace(
            ")", ""
        )

        disease_name = disease_name.replace(
            "Two-spotted",
            "Two Spotted"
        )

        disease_name = " ".join(
            disease_name.split()
        )

        disease_name = disease_name.strip()

        print(
            "CLEANED DISEASE NAME:",
            disease_name
        )

        # ==========================================
        # DEFAULT VALUES
        # ==========================================

        remedy = (
            "No remedy information available."
        )

        prevention = (
            "No prevention information available."
        )

        chemical_remedy = (
            "No chemical treatment information available."
        )

        description = ""

        database_disease_name = disease_name

        # ==========================================
        # STEP 3: CONNECT ORACLE
        # ==========================================

        connection = get_db_connection()
        cursor = connection.cursor()

        # ==========================================
        # STEP 4: FIND DISEASE
        # ==========================================

        cursor.execute(
            """
            SELECT
                d.disease_id,
                d.disease_name,
                d.description
            FROM DISEASES d
            JOIN PLANTS p
                ON d.plant_id = p.plant_id
            WHERE LOWER(p.plant_name) = LOWER(:plant_name)
            AND LOWER(d.disease_name) = LOWER(:disease_name)
            """,
            {
                "plant_name": plant_name,
                "disease_name": disease_name
            }
        )

        disease = cursor.fetchone()

        if disease:

            disease_id = disease[0]

            database_disease_name = disease[1]

            description = disease[2] or ""
            remedy_data=None
                        # ======================================
            # STEP 5: FIND SEVERITY-BASED REMEDY
            # ======================================

            if "healthy" in database_disease_name.lower():
                remedy = "No treatment needed based on this prediction."
                prevention = (
                    "Continue regular watering, provide suitable sunlight, "
                    "and monitor the plant for changes."
                )
                chemical_remedy = (
                    "Chemical treatment is not indicated for a healthy prediction."
                )

            else:
                cursor.execute(
                    """
                    SELECT
                        remedy,
                        prevention,
                        chemical_remedy
                    FROM REMEDIES
                    WHERE disease_id = :disease_id
                    AND (
                        UPPER(TRIM(severity_level)) =
                            UPPER(TRIM(:severity))
                        OR severity_level IS NULL
                    )
                    ORDER BY
                        CASE
                            WHEN UPPER(TRIM(severity_level)) =
                                UPPER(TRIM(:severity))
                            THEN 0
                            ELSE 1
                        END,
                        remedy_id
                    FETCH FIRST 1 ROW ONLY
                    """,
                    {
                        "disease_id": disease_id,
                        "severity": severity_result["severity"]
                    }
                )
                remedy_data = None
                remedy_data = cursor.fetchone()

                if remedy_data:
                    remedy = (
                        remedy_data[0]
                        or "No remedy information available."
                    )
                    prevention = (
                        remedy_data[1]
                        or "No prevention information available."
                    )
                    chemical_remedy = (
                        remedy_data[2]
                        or "Consult a local agricultural expert for suitable treatment."
                    )

            print("SEVERITY:", severity_result["severity"])
            print("REMEDY:", remedy)
            print("PREVENTION:", prevention)
            print("CHEMICAL REMEDY:", chemical_remedy)

            print("====================================")
            print("DISEASE ID:", disease_id)
            print("REMEDY DATA:", remedy_data)
            print("REMEDY:", remedy)
            print("PREVENTION:", prevention)
            print(
                "CHEMICAL REMEDY:",
                chemical_remedy
            )
            print("====================================")
        # ==========================================
# STEP 6: SAVE PREDICTION HISTORY
# ==========================================

            cursor.execute(
                """
                INSERT INTO PREDICTION_HISTORY
                (
                    user_id,
                    plant_name,
                    disease_name,
                    confidence,
                    image_path,
                    severity_level
                )
                VALUES
                (
                    :user_id,
                    :plant_name,
                    :disease_name,
                    :confidence,
                    :image_path,
                    :severity_level
                )
                """,
                {
                    "user_id": session["user_id"],
                    "plant_name": plant_name,
                    "disease_name": database_disease_name,
                    "confidence": round(confidence, 2),
                    "image_path": image_path.replace("\\", "/"),
                    "severity_level": severity_result["severity"]
                }
            )

            print("Prediction history with severity saved successfully!")

        # ==========================================
        # STEP 7: CREATE NOTIFICATION DATA
        # ==========================================

        confidence_value = round(
            confidence,
            2
        )

        # ------------------------------------------
        # NOTIFICATION TO ADMIN
        # ------------------------------------------

        notify_all_admins(
            cursor=cursor,
            title="New Disease Prediction",
            message=(
                f"{session['full_name']} predicted "
                f"{plant_name} - "
                f"{database_disease_name} "
                f"with {confidence_value:.2f}% confidence."
            ),
            notification_type="prediction",
            sender_id=session["user_id"]
        )

        # ------------------------------------------
        # NOTIFICATION TO USER
        # ------------------------------------------

        add_notification(
            cursor=cursor,
            user_id=session["user_id"],
            title="Prediction Completed",
            message=(
                f"Your {plant_name} prediction is "
                f"{database_disease_name} "
                f"with {confidence_value:.2f}% confidence."
            ),
            notification_type="prediction",
            sender_id=session["user_id"]
        )

        # ==========================================
        # STEP 8: COMMIT EVERYTHING
        # ==========================================

        connection.commit()

        print(
            "Prediction notifications created successfully!"
        )

        # ==========================================
        # STEP 9: SHOW RESULT ON DETECT PAGE
        # ==========================================

        latest_prediction = {

            "plant_name": plant_name,

            "disease_name": database_disease_name,

            "confidence": confidence_value,

            "image_path": image_path.replace(
                "\\",
                "/"
            ),

            "description": description,

            "remedy": remedy,

            "prevention": prevention,

            "chemical_remedy": chemical_remedy,
            "severity": severity_result["severity"],
            "affected_percentage": severity_result["affected_percentage"],
            "severity_note": severity_result["note"]
        }

        return render_template(
            "detect.html",
            latest_prediction=latest_prediction
        )

    # ==============================================
    # ERROR HANDLING
    # ==============================================

    except Exception as error:

        print(
            "Prediction/Database Error:",
            error
        )

        if connection:
            connection.rollback()

        flash(
            "Unable to process the prediction."
        )

        return redirect(
            url_for("dashboard")
        )

    # ==============================================
    # CLOSE DATABASE
    # ==============================================

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        current_user_id = session["user_id"]

        print("====================================")
        print("CURRENT SESSION USER ID:", current_user_id)
        print("====================================")

        cursor.execute(
            """
            SELECT
                prediction_id,
                user_id,
                plant_name,
                disease_name,
                confidence,
                image_path,
                predicted_at
            FROM PREDICTION_HISTORY
            WHERE user_id = :user_id
            ORDER BY predicted_at DESC
            """,
            {
                "user_id": current_user_id
            }
        )

        history_data = cursor.fetchall()

        print("HISTORY ROWS FOUND:", len(history_data))

        for row in history_data:
            print("HISTORY:", row)

        return render_template(
            "history.html",
            history=history_data
        )

    except psycopg2.Error as error:

        print("History Error:", error)

        flash("Unable to load prediction history.")
        return redirect(url_for("dashboard"))

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()
@app.route("/prediction/<int:prediction_id>")
def prediction_details(prediction_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                ph.prediction_id,
                ph.plant_name,
                ph.disease_name,
                ph.confidence,
                ph.image_path,
                ph.predicted_at,
                d.description,
                r.remedy,
                r.prevention
            FROM PREDICTION_HISTORY ph
            LEFT JOIN PLANTS p
                ON LOWER(p.plant_name) = LOWER(ph.plant_name)
            LEFT JOIN DISEASES d
                ON d.plant_id = p.plant_id
                AND LOWER(d.disease_name) = LOWER(ph.disease_name)
            LEFT JOIN REMEDIES r
                ON r.disease_id = d.disease_id
            WHERE ph.prediction_id = :prediction_id
            AND ph.user_id = :user_id
        """, {
            "prediction_id": prediction_id,
            "user_id": session["user_id"]
        })

        prediction = cursor.fetchone()

        if not prediction:
            flash("Prediction not found.")
            return redirect(url_for("history"))

        return render_template(
            "prediction_details.html",
            prediction=prediction
        )

    except psycopg2.Error as error:
        print("Prediction Details Error:", error)
        flash("Unable to load prediction details.")
        return redirect(url_for("history"))

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
            
@app.route("/plant-library")
def plant_library():
 
    if "user_id" not in session:
        return redirect(url_for("login"))
 
    connection = None
    cursor = None
 
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
 
        cursor.execute("""
            SELECT
                plant_id,
                plant_name,
                tamil_name,
                scientific_name,
                image_path
            FROM PLANTS
            ORDER BY plant_id
        """)
 
        plants = cursor.fetchall()
 
        return render_template(
            "plant_library.html",
            plants=plants
        )
 
    except Exception as error:
 
        print("Plant Library Error:", repr(error))
 
        if connection:
            connection.rollback()
 
        flash("Unable to load plant library.")
        return redirect(url_for("dashboard"))
 
    finally:
 
        if cursor:
            cursor.close()
 
        if connection:
            connection.close()
# ============================================================
# ADMIN DASHBOARD
# ============================================================
@app.route("/admin-dashboard")
def admin_dashboard():

    if session.get("role") != "ADMIN":
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        # -----------------------------------------
        # 0. UNREAD NOTIFICATION COUNT
        # -----------------------------------------
        cursor.execute("""
            SELECT COUNT(*)
            FROM NOTIFICATIONS
            WHERE user_id = :user_id
            AND is_read = 0
        """, {
            "user_id": session["user_id"]
        })

        unread_notifications = cursor.fetchone()[0] or 0

        # -----------------------------------------
        # 1. TOTAL USERS
        # -----------------------------------------
        cursor.execute("""
            SELECT COUNT(*)
            FROM USERS
        """)

        total_users = cursor.fetchone()[0]

        # -----------------------------------------
        # 2. TOTAL PREDICTIONS
        # -----------------------------------------
        cursor.execute("""
            SELECT COUNT(*)
            FROM PREDICTION_HISTORY
        """)

        total_predictions = cursor.fetchone()[0]

        # -----------------------------------------
        # 3. HEALTHY PREDICTIONS
        # -----------------------------------------
        cursor.execute("""
            SELECT COUNT(*)
            FROM PREDICTION_HISTORY
            WHERE UPPER(TRIM(DISEASE_NAME)) = 'HEALTHY'
        """)

        healthy_predictions = cursor.fetchone()[0]

        # -----------------------------------------
        # 4. DISEASED PREDICTIONS
        # -----------------------------------------
        diseased_predictions = (
            total_predictions - healthy_predictions
        )

        # -----------------------------------------
        # 5. AVERAGE CONFIDENCE
        # -----------------------------------------
        cursor.execute("""
            SELECT NVL(AVG(CONFIDENCE), 0)
            FROM PREDICTION_HISTORY
        """)

        avg_confidence = cursor.fetchone()[0]

        # -----------------------------------------
        # 6. TOTAL DISEASES
        # -----------------------------------------
        cursor.execute("""
            SELECT COUNT(*)
            FROM DISEASES
        """)

        total_diseases = cursor.fetchone()[0]

        # -----------------------------------------
        # 7. TOTAL REMEDIES
        # -----------------------------------------
        cursor.execute("""
            SELECT COUNT(*)
            FROM REMEDIES
        """)

        total_remedies = cursor.fetchone()[0]

        # -----------------------------------------
        # 8. DISEASE DISTRIBUTION
        # -----------------------------------------
        cursor.execute("""
            SELECT
                DISEASE_NAME,
                COUNT(*) AS TOTAL
            FROM PREDICTION_HISTORY
            GROUP BY DISEASE_NAME
            ORDER BY TOTAL DESC
        """)

        disease_distribution = cursor.fetchall()

        # -----------------------------------------
        # 9. PLANT DISTRIBUTION
        # -----------------------------------------
        cursor.execute("""
            SELECT
                PLANT_NAME,
                COUNT(*) AS TOTAL
            FROM PREDICTION_HISTORY
            GROUP BY PLANT_NAME
            ORDER BY TOTAL DESC
        """)

        plant_distribution = cursor.fetchall()

        # -----------------------------------------
        # 10. RECENT PREDICTIONS
        # -----------------------------------------
        cursor.execute("""
            SELECT
                p.prediction_id,
                u.full_name,
                p.plant_name,
                p.disease_name,
                p.confidence,
                p.predicted_at
            FROM PREDICTION_HISTORY p
            LEFT JOIN USERS u
                ON p.user_id = u.user_id
            ORDER BY p.predicted_at DESC
            FETCH FIRST 10 ROWS ONLY
        """)

        recent_predictions = cursor.fetchall()

        # -----------------------------------------
        # 11. REGISTERED USERS
        # -----------------------------------------
        cursor.execute("""
            SELECT
                user_id,
                full_name,
                email,
                role,
                created_at
            FROM USERS
            ORDER BY created_at DESC
        """)

        users = cursor.fetchall()

        # -----------------------------------------
        # 12. SEND DATA TO TEMPLATE
        # -----------------------------------------
        return render_template(
            "admin_dashboard.html",

            unread_notifications=unread_notifications,

            total_users=total_users,
            total_predictions=total_predictions,

            healthy_predictions=healthy_predictions,
            diseased_predictions=diseased_predictions,

            avg_confidence=float(
                avg_confidence or 0
            ),

            total_diseases=total_diseases,
            total_remedies=total_remedies,

            disease_distribution=disease_distribution,
            plant_distribution=plant_distribution,

            recent_predictions=recent_predictions,
            users=users
        )

    except psycopg2.Error as error:

        print(
            "Admin Dashboard Oracle Error:",
            error
        )

        return f"""
        <h2>Admin Dashboard Database Error</h2>
        <p>{error}</p>
        """

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/admin/send-message", methods=["POST"])
def admin_send_message():

    # -----------------------------------------
    # ADMIN ONLY
    # -----------------------------------------
    if session.get("role") != "ADMIN":
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:

        # -----------------------------------------
        # GET FORM DATA
        # -----------------------------------------
        user_id = request.form.get("user_id", "").strip()
        title = request.form.get("title", "").strip()
        message = request.form.get("message", "").strip()

        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------
        if not user_id or not message:
            flash("Please select a user and enter a message.")
            return redirect(url_for("admin_dashboard"))

        connection = get_db_connection()
        cursor = connection.cursor()

        # -----------------------------------------
        # CHECK USER EXISTS
        # -----------------------------------------
        cursor.execute("""
            SELECT user_id, full_name
            FROM USERS
            WHERE user_id = :user_id
        """, {
            "user_id": int(user_id)
        })

        user = cursor.fetchone()

        if not user:

            flash("Selected user was not found.")

            return redirect(
                url_for("admin_dashboard")
            )

        target_user_id = user[0]
        target_user_name = user[1]

        # -----------------------------------------
        # DEFAULT TITLE
        # -----------------------------------------
        if not title:
            title = "Message from Admin"

        # -----------------------------------------
        # CREATE USER NOTIFICATION
        # -----------------------------------------
        add_notification(
            cursor=cursor,
            user_id=target_user_id,
            title=title,
            message=message,
            notification_type="message",
            sender_id=session.get("user_id")
        )

        # -----------------------------------------
        # COMMIT
        # -----------------------------------------
        connection.commit()

        print("====================================")
        print("ADMIN MESSAGE SENT")
        print("TO USER:", target_user_name)
        print("USER ID:", target_user_id)
        print("TITLE:", title)
        print("MESSAGE:", message)
        print("====================================")

        flash(
            f"Message sent successfully to {target_user_name}."
        )

        return redirect(
            url_for("admin_dashboard")
        )

    except psycopg2.Error as error:

        print(
            "Admin Message Oracle Error:",
            error
        )

        if connection:
            connection.rollback()

        flash(
            "Unable to send message."
        )

        return redirect(
            url_for("admin_dashboard")
        )

    except Exception as error:

        print(
            "Admin Message Error:",
            error
        )

        if connection:
            connection.rollback()

        flash(
            "Unable to send message."
        )

        return redirect(
            url_for("admin_dashboard")
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()
            
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None
    user_id = session["user_id"]

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == "POST":
            action = request.form.get("action", "")

            # -----------------------------
            # UPDATE PROFILE PHOTO
            # -----------------------------
            if action == "update_photo":
                photo = request.files.get("profile_photo")

                if not photo or not photo.filename:
                    flash("Please select a profile photo.")
                    return redirect(url_for("profile"))

                if not allowed_profile_image(photo.filename):
                    flash("Upload JPG, JPEG, PNG, or WEBP only.")
                    return redirect(url_for("profile"))

                extension = photo.filename.rsplit(".", 1)[1].lower()
                filename = f"{uuid.uuid4().hex}.{extension}"
                photo_path = os.path.join(
                    app.config["PROFILE_UPLOAD_FOLDER"], filename
                )

                photo.save(photo_path)

                relative_path = f"profile_photos/{filename}"

                cursor.execute("""
                    UPDATE USERS
                    SET PROFILE_PHOTO = :photo
                    WHERE USER_ID = :user_id
                """, {
                    "photo": relative_path,
                    "user_id": user_id
                })

                connection.commit()
                flash("Profile photo updated successfully!")

            # -----------------------------
            # CHANGE PASSWORD
            # -----------------------------
            elif action == "change_password":
                current_password = request.form.get("current_password", "")
                new_password = request.form.get("new_password", "")
                confirm_password = request.form.get("confirm_password", "")

                if not current_password or not new_password or not confirm_password:
                    flash("Please fill in all password fields.")
                    return redirect(url_for("profile"))

                if len(new_password) < 8:
                    flash("New password must be at least 8 characters.")
                    return redirect(url_for("profile"))

                if new_password != confirm_password:
                    flash("New passwords do not match.")
                    return redirect(url_for("profile"))

                cursor.execute("""
                    SELECT PASSWORD_HASH
                    FROM USERS
                    WHERE USER_ID = :user_id
                """, {"user_id": user_id})

                password_row = cursor.fetchone()

                if not password_row or not check_password_hash(
                    password_row[0], current_password
                ):
                    flash("Current password is incorrect.")
                    return redirect(url_for("profile"))

                new_password_hash = generate_password_hash(new_password)

                cursor.execute("""
                    UPDATE USERS
                    SET PASSWORD_HASH = :password_hash
                    WHERE USER_ID = :user_id
                """, {
                    "password_hash": new_password_hash,
                    "user_id": user_id
                })

                connection.commit()
                flash("Password changed successfully!")

            else:
                flash("Invalid profile action.")

            return redirect(url_for("profile"))

        # -----------------------------
        # LOAD USER PROFILE
        # -----------------------------
        cursor.execute("""
            SELECT
                USER_ID,
                FULL_NAME,
                EMAIL,
                ROLE,
                CREATED_AT,
                PROFILE_PHOTO
            FROM USERS
            WHERE USER_ID = :user_id
        """, {"user_id": user_id})

        user = cursor.fetchone()

        if not user:
            session.clear()
            return redirect(url_for("login"))

        return render_template("profile.html", user=user)

    except Exception as error:
        print("Profile Error:", error)

        if connection:
            connection.rollback()

        flash("Unable to update profile.")

        return redirect(url_for("profile"))

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
PLANT_DETAILS = {
    1: ("Tomato", "தக்காளி", "Solanum lycopersicum", "tomato.jpg"),
    2: ("Potato", "உருளைக்கிழங்கு", "Solanum tuberosum", "potato.jpg"),
    3: ("Pepper", "மிளகாய்", "Capsicum annuum", "pepper.jpg"),
    21: ("Apple", "ஆப்பிள்", "Malus domestica", "apple.jpg"),
    22: ("Blueberry", "புளூபெர்ரி", "Vaccinium corymbosum", "blueberry.jpg"),
    23: ("Cherry", "செர்ரி", "Prunus avium", "cherry.jpg"),
    24: ("Corn", "மக்காச்சோளம்", "Zea mays", "corn.jpg"),
    25: ("Grape", "திராட்சை", "Vitis vinifera", "grape.jpg"),
    26: ("Orange", "ஆரஞ்சு", "Citrus sinensis", "orange.jpg"),
    27: ("Peach", "பீச்", "Prunus persica", "peach.jpg"),
    28: ("Raspberry", "ராஸ்பெர்ரி", "Rubus idaeus", "raspberry.jpg"),
    29: ("Soybean", "சோயாபீன்", "Glycine max", "soybean.jpg"),
    30: ("Squash", "பூசணிக்காய்", "Cucurbita spp.", "squash.jpg"),
    31: ("Strawberry", "ஸ்ட்ராபெர்ரி", "Fragaria x ananassa", "strawberry.jpg")
}
 


@app.route("/update-plant-details")
def update_plant_details():
    if session.get("role") != "ADMIN":
        return redirect(url_for("login"))
 
    connection = None
    cursor = None
 
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
 
        for plant_id, details in PLANT_DETAILS.items():
 
            english_name, tamil_name, scientific_name, image_filename = details
 
            cursor.execute(
                """
                UPDATE PLANTS
                SET
                    PLANT_NAME = :english_name,
                    TAMIL_NAME = :tamil_name,
                    SCIENTIFIC_NAME = :scientific_name,
                    IMAGE_PATH = :image_filename
                WHERE PLANT_ID = :plant_id
                """,
                {
                    "english_name": english_name,
                    "tamil_name": tamil_name,
                    "scientific_name": scientific_name,
                    "image_filename": image_filename,
                    "plant_id": plant_id
                }
            )
 
        connection.commit()
 
        return """
        <h2>Plant details updated successfully!</h2>
        <p>All 14 plants now have English, Tamil, Scientific names and images.</p>
        <a href="/plant-library">Go to Plant Library</a>
        """
 
    except Exception as error:
 
        print("Plant Details Update Error:", error)
 
        if connection:
            connection.rollback()
 
        return f"""
        <h2>Update failed</h2>
        <p>{error}</p>
        """
 
    finally:
 
        if cursor:
            cursor.close()
 
        if connection:
            connection.close()
 
CARE_GUIDE = {
    "Tomato": {
        "water": {"en": "Water deeply 2-3 times a week. Keep soil moist, not soggy.", "ta": "வாரத்திற்கு 2-3 முறை ஆழமாக நீர் பாய்ச்சவும். மண் ஈரமாக இருக்கட்டும், ஆனால் தண்ணீர் தேங்கக்கூடாது."},
        "sunlight": {"en": "6-8 hours of direct sunlight daily.", "ta": "தினமும் 6-8 மணி நேரம் நேரடி வெயில் தேவை."},
        "soil": {"en": "Well-drained, loamy soil. pH 6.0-6.8.", "ta": "நன்கு வடிகால் உள்ள களிமண். pH 6.0-6.8."},
        "fertilizer": {"en": "NPK 10-10-10 every 2 weeks after flowering.", "ta": "பூத்த பிறகு 2 வாரத்திற்கு ஒருமுறை NPK 10-10-10 உரம்."},
        "season": {"en": "Best: June-Sep and Dec-Mar", "ta": "சிறந்த பருவம்: ஜூன்-செப், டிச்-மார்"},
    },
    "Potato": {
        "water": {"en": "Regular watering, especially during tuber formation.", "ta": "கிழங்கு உருவாகும் நேரத்தில் தொடர்ந்து நீர் பாய்ச்சவும்."},
        "sunlight": {"en": "Full sun, 6 hours minimum.", "ta": "குறைந்தது 6 மணி நேரம் வெயில் தேவை."},
        "soil": {"en": "Loose, sandy loam soil. pH 5.0-6.0.", "ta": "தளர்வான மணல் கலந்த களிமண். pH 5.0-6.0."},
        "fertilizer": {"en": "Potassium-rich fertilizer during planting.", "ta": "நடும்போது பொட்டாஷ் நிறைந்த உரம் இடவும்."},
        "season": {"en": "Best: Oct-Jan", "ta": "சிறந்த பருவம்: அக்-ஜன"},
    },
    # meedhi 12 plants-kum inga add pannunga — Tamil translation help venum-na sollunga!
}

@app.route('/plant/<int:plant_id>')
def plant_detail(plant_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Get plant
        cursor.execute("""
            SELECT plant_id, plant_name,image_path
            FROM PLANTS
            WHERE plant_id = :plant_id
        """, {
            "plant_id": plant_id
        })

        plant = cursor.fetchone()

        if not plant:
            flash("Plant not found.")
            return redirect(url_for("plant_library"))

        # Get diseases, description and remedies
        cursor.execute("""
            SELECT
                d.disease_name,
                d.description,
                r.remedy,
                r.prevention
            FROM DISEASES d
            LEFT JOIN REMEDIES r
                ON d.disease_id = r.disease_id
            WHERE d.plant_id = :plant_id
            ORDER BY d.disease_name
        """, {
            "plant_id": plant_id
        })

        diseases = cursor.fetchall()

        print("Plant:", plant)
        print("Diseases found:", len(diseases))

        return render_template(
            "plant_detail.html",
            plant=plant,
            diseases=diseases,
            tamil_guide=TAMIL_GUIDE
            )
    except psycopg2.Error as error:

        print("Plant Detail Error:", error)
        flash("Unable to load plant details.")
        return redirect(url_for("plant_library"))

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/admin/send-message", methods=["GET"])
def admin_send_message_page():
    if "user_id" not in session or session.get("role") != "ADMIN":
        flash("Admin access required.")
        return redirect(url_for("login"))

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT user_id, full_name, email
            FROM USERS
            ORDER BY full_name
        """)
        users = cursor.fetchall()

        return render_template(
            "admin_send_message.html",
            users=users
        )

    except Exception as error:
        print("Send Message Page Error:", repr(error))
        flash("Unable to open Send Message page.")
        return redirect(url_for("admin_dashboard"))

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
@app.route("/admin/add-plant", methods=["GET"])
def add_plant():
    if "user_id" not in session or session.get("role") != "ADMIN":
        flash("Admin access required.")
        return redirect(url_for("login"))

    return render_template("admin_add_plant.html")
@app.route("/admin/add-plant", methods=["POST"])
def admin_add_plant():
    if "user_id" not in session or session.get("role") != "ADMIN":
        flash("Admin access required.")
        return redirect(url_for("login"))

    connection = None
    cursor = None
    image_path = None

    try:
        plant_name = request.form.get("plant_name", "").strip()
        tamil_name = request.form.get("tamil_name", "").strip()
        scientific_name = request.form.get("scientific_name", "").strip()
        description = request.form.get("description", "").strip()
        image = request.files.get("plant_image")

        if not plant_name:
            flash("Please enter the plant name.")
            return redirect(url_for("admin_dashboard"))

        if len(plant_name) > 100:
            flash("Plant name must be within 100 characters.")
            return redirect(url_for("admin_dashboard"))

        if not image or not image.filename:
            flash("Please select a plant image.")
            return redirect(url_for("admin_dashboard"))

        allowed_extensions = {"jpg", "jpeg", "png", "webp"}
        original_name = secure_filename(image.filename)

        if (
            "." not in original_name
            or original_name.rsplit(".", 1)[1].lower()
            not in allowed_extensions
        ):
            flash("Upload JPG, JPEG, PNG or WEBP image.")
            return redirect(url_for("admin_dashboard"))

        # Save image inside static/plant-images
        upload_folder = os.path.join(
            app.root_path, "static", "plant-images"
        )
        os.makedirs(upload_folder, exist_ok=True)

        extension = original_name.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{extension}"
        image_path = os.path.join(upload_folder, filename)

        image.save(image_path)

        # Store a path relative to the static folder
        database_image_path = f"plant-images/{filename}"

        connection = get_db_connection()
        cursor = connection.cursor()

        # Use the existing Oracle sequence if one exists;
        # otherwise, generate an ID from the current maximum.
        cursor.execute("""
            SELECT NVL(MAX(PLANT_ID), 0) + 1
            FROM PLANTS
        """)
        new_plant_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO PLANTS (
                PLANT_ID,
                PLANT_NAME,
                DESCRIPTION,
                CREATED_AT,
                TAMIL_NAME,
                SCIENTIFIC_NAME,
                IMAGE_PATH
            )
            VALUES (
                :plant_id,
                :plant_name,
                :description,
                SYSTIMESTAMP,
                :tamil_name,
                :scientific_name,
                :image_path
            )
        """, {
            "plant_id": new_plant_id,
            "plant_name": plant_name,
            "description": description or None,
            "tamil_name": tamil_name or None,
            "scientific_name": scientific_name or None,
            "image_path": database_image_path
        })

        connection.commit()
        image_path = None  # Keep uploaded file after successful insert

        flash(f"{plant_name} added to Plant Library successfully!")

    except Exception as error:
        print("Admin Add Plant Error:", repr(error))

        if connection:
            connection.rollback()

        if image_path and os.path.exists(image_path):
            os.remove(image_path)

        flash("Unable to add plant. Please check the application logs.")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return redirect(url_for("admin_dashboard"))


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)