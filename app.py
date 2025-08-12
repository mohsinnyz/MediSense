import streamlit as st
import joblib
import requests
from io import BytesIO
import numpy as np
import re

# ------------------------
# Hugging Face Repo
# ------------------------
REPO_URL = "https://huggingface.co/mohsinnyz/Disease-Guider/resolve/main"

# ------------------------
# File loader with checks
# ------------------------
def load_file_from_hf(filename):
    url = f"{REPO_URL}/{filename}"
    response = requests.get(url)
    if response.status_code != 200:
        raise FileNotFoundError(f"Failed to fetch {filename} (status {response.status_code})")
    return joblib.load(BytesIO(response.content))

@st.cache_resource
def load_model_files():
    try:
        model = load_file_from_hf("model.pkl")
        label_encoder = load_file_from_hf("label_encoder.pkl")
        symptom_encoder = load_file_from_hf("symptom_encoder.pkl")
        symptom_list = load_file_from_hf("symptom_list.pkl")
        return model, label_encoder, symptom_encoder, symptom_list
    except Exception as e:
        st.error(f"Failed to load model files: {e}")
        st.stop()

model, label_encoder, symptom_encoder, symptom_list = load_model_files()

# ------------------------
# Page Config
# ------------------------
st.set_page_config(
    page_title="MediSense - Mohsin Nyz",
    page_icon="🧬",
    layout="wide"
)

# ------------------------
# Custom CSS
# ------------------------
st.markdown("""
<style>
/* Global Styles & Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
html, body, [class*="st-emotion-cache"] {
    font-family: 'Roboto', sans-serif;
    color: #E0E0E0;
}

/* Header & Title Styling */
.main-header {
    text-align: center;
    padding: 2rem 0 1rem;
    background-image: linear-gradient(to right, #1E3A8A, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.main-header h1 {
    font-family: 'Times New Roman', Times, serif;
    font-size: 5rem;
    font-weight: bold;
    margin-bottom: 0;
}
.main-header h3 {
    font-weight: normal;
    color: #9CA3AF;
    margin-top: 0;
    font-size: 1.5rem;
}

/* Containers & Cards */
.st-emotion-cache-1pxx9r2 { /* This targets the main container */
    background-color: #1E293B;
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
}

/* Prediction Result Boxes */
.prediction-info {
    display: flex;
    justify-content: space-around;
    gap: 20px;
    margin-top: 10px;
}
.prediction-box {
    background-color: #374151;
    border: 1px solid #4B5563;
    padding: 15px 25px;
    border-radius: 10px;
    text-align: center;
    flex: 1;
    transition: transform 0.2s;
}
.prediction-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.prediction-box p {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
    color: #D1D5DB;
}
.prediction-box small {
    color: #9CA3AF;
    font-size: 0.9rem;
}

/* Section Titles & Content */
.section-title {
    font-size: 1.2rem;
    font-weight: bold;
    color: #93C5FD;
    margin-top: 15px;
    margin-bottom: 8px;
    border-bottom: 2px solid #1E3A8A;
    padding-bottom: 5px;
}
.section-content {
    background-color: #2D3A4B;
    padding: 15px;
    border-radius: 8px;
    color: #E0E0E0;
    font-size: 1rem;
    line-height: 1.6;
}

/* Streamlit Component Customizations */
.stMultiSelect > label {
    font-weight: bold;
    color: #D1D5DB;
    font-size: 1.1rem;
}
.stMultiSelect > div > div > div {
    background-color: #374151;
    border: 1px solid #4B5563;
    border-radius: 8px;
    color: #E0E0E0;
}
.stMultiSelect [data-baseweb="select"] div {
    background-color: #374151;
    color: #E0E0E0;
}
.st-emotion-cache-1g814f { /* Button styling */
    background-color: #3B82F6 !important;
    border-color: #3B82F6 !important;
    color: white !important;
    font-weight: bold !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    transition: background-color 0.3s;
}
.st-emotion-cache-1g814f:hover {
    background-color: #2563EB !important;
    border-color: #2563EB !important;
}

/* Disclaimer Styling */
.st-emotion-cache-17l028h p { /* Targets the error box text */
    font-size: 1rem;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

# ------------------------
# Header
# ------------------------
st.markdown("""
<div class="main-header">
    <h1>🧬 MediSense</h1>
    <h3>Your AI-powered Symptom Checker & Medical Assistant</h3>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.error(
    "⚠️ **Disclaimer:** This tool is for **informational purposes only**. "
    "**It is not a substitute for professional medical advice, diagnosis, or treatment**. "
    "**Always consult a licensed medical professional**."
)

st.markdown("---")

# ------------------------
# Main App Container
# ------------------------
with st.container():
    st.subheader("📝 Symptom Reporting")
    
    selected_symptoms = st.multiselect(
        "**Select **3 to 5 symptoms** from the list below to get an AI-powered prediction.**",
        options=symptom_list,
        placeholder="Choose symptoms...",
        max_selections=5
    )
    
    predict_btn = st.button("🔍 Predict Disease", type="primary", use_container_width=True)

st.markdown("---")

# ------------------------
# Prediction & Results
# ------------------------
if predict_btn:
    if len(selected_symptoms) < 3:
        st.error("❌ Please select at least 3 symptoms.")
    else:
        gemini_api_key = st.secrets.get("GEMINI_API_KEY")

        # Start of the modified section
        loading_placeholder = st.empty()
        loading_placeholder.markdown(
            "<div style='color:#9CA3AF;font-weight:bold;'>⏳ Running AI prediction...</div>",
            unsafe_allow_html=True
        )

        symptom_to_idx = {s.lower().strip(): i for i, s in enumerate(symptom_list)}
        input_vector = np.zeros(len(symptom_list))
        for symptom in selected_symptoms:
            idx = symptom_to_idx.get(symptom.lower().strip())
            if idx is not None:
                input_vector[idx] = 1
        
        probabilities = model.predict_proba([input_vector])[0]
        top_index = np.argmax(probabilities)
        
        predicted_disease = label_encoder.inverse_transform([top_index])[0]
        confidence = probabilities[top_index] * 100

        # Clear the first loading message
        loading_placeholder.empty()

        st.subheader("📊 Prediction Result")
        st.markdown(f"""
        <div class='prediction-result-container'>
            <div class='prediction-info'>
                <div class='prediction-box'>
                    <small>Predicted Disease</small>
                    <p>{predicted_disease}</p>
                </div>
                <div class='prediction-box'>
                    <small>AI Confidence</small>
                    <p>{confidence:.2f}%</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
            
        if gemini_api_key:
            # The medical card now wraps all the Gemini-related content
            st.markdown(f"<div class='medical-card'>", unsafe_allow_html=True)
            st.markdown(f"<h3>🩺 About {predicted_disease}</h3>", unsafe_allow_html=True)
            
            loading_placeholder_gemini = st.empty()
            loading_placeholder_gemini.markdown(
                "<div style='color:#9CA3AF;font-weight:bold;'>⏳ Analysing disease details...</div>",
                unsafe_allow_html=True
            )

            prompt = f"""
            Provide:
            1. Medical Description: A brief medical description of {predicted_disease}.
            2. Recommended next steps: Safe, general advice.
            3. Possible home remedies: For mild cases (with disclaimers).
            4. When to seek urgent medical care: Clear red flags.
            Keep it concise, structured, and medically accurate. Use Markdown for lists and emphasis.
            """
            
            headers = {"Content-Type": "application/json"}
            body = {"contents": [{"parts": [{"text": prompt}]}]}
            
            try:
                # Use gemini-1.5-flash which is a more powerful model for this task.
                response = requests.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
                    headers=headers,
                    params={"key": gemini_api_key},
                    json=body,
                    timeout=15
                )
                if response.status_code != 200:
                    st.error(f"Gemini API Error {response.status_code}: {response.text}")
                else:
                    result = response.json()
                    if "candidates" in result:
                        llm_response_text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                        loading_placeholder_gemini.empty()
                        
                        # Use Markdown for all content rendering
                        st.markdown("""
                            <style>
                            .section-title {
                                font-size: 1.2rem;
                                font-weight: bold;
                                color: #93C5FD;
                                margin-top: 20px;
                                margin-bottom: 6px;
                            }
                            .section-content {
                                background-color: #2D3A4B;
                                padding: 12px;
                                border-radius: 8px;
                                font-size: 1rem;
                                line-height: 1.6;
                                margin-bottom: 14px;
                            }
                            </style>
                        """, unsafe_allow_html=True)

                        # Regex to split content by numbered headings.
                        sections = re.split(r'\n\s*(\d+\.)\s*([^\n:]+:\s*)', llm_response_text)

                        if len(sections) > 1:
                            emoji_map = {
                                'Medical Description': '📝',
                                'Recommended next steps': '➡️',
                                'Possible home remedies': '🌿',
                                'When to seek urgent medical care': '🚨'
                            }
                            
                            for i in range(1, len(sections), 3):
                                number = sections[i].strip()
                                title_text_part = sections[i+1].strip() if i+1 < len(sections) else ''
                                content = sections[i+2].strip() if i+2 < len(sections) else ''
                                
                                emoji = emoji_map.get(title_text_part.replace(":", "").strip(), '•')
                                final_title_html = f"<div class='section-title'>{emoji} <strong>{number} {title_text_part}</strong></div>"
                                
                                st.markdown(final_title_html, unsafe_allow_html=True)
                                st.markdown(content)
                        else:
                            st.markdown(llm_response_text)
                    else:
                        st.error("❌ Gemini API returned no valid text.")
            except Exception as e:
                loading_placeholder_gemini.empty()
                st.error(f"Failed to fetch description: {e}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("💡 Gemini API key not found in secrets.toml. Disease care suggestion feature is unavailable.")