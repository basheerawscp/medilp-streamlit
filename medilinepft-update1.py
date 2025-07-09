### AI Health Checker - Streamlit App (Together.ai + UAE Clinic Recommendations)
# app.py

import streamlit as st
import os
import requests

st.set_page_config(page_title="AI Health Checker", page_icon="🩺")

st.title("🩺 AI Health Checker")
st.markdown("This tool provides **AI-powered, non-diagnostic** health advice based on your symptoms.\n\n⚠️ This is not a substitute for professional medical advice.")

# UAE clinic mapping (basic version)
uae_clinics = {
    "Dubai": ["Aster Clinic – Al Nahda", "Mediclinic – Dubai Mall", "NMC Specialty Hospital – Deira"],
    "Abu Dhabi": ["Burjeel Hospital", "NMC Royal – Khalifa City", "LLH Hospital – Musaffah"],
    "Sharjah": ["Thumbay Hospital", "Zulekha Hospital", "Al Zahra Hospital"]
}

# Collect user input
with st.form("health_form"):
    age = st.number_input("Your Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    location = st.selectbox("Your Location (UAE only)", list(uae_clinics.keys()))
    duration = st.selectbox("How long have you had the symptoms?", ["< 1 day", "1-3 days", "> 1 week"])
    symptoms = st.text_area("Describe your symptoms")
    history = st.text_input("Any pre-existing conditions (e.g., diabetes, asthma)?")
    medications = st.text_input("Medications you are currently taking (if any)")
    habits = st.radio("Do you smoke or drink alcohol?", ["No", "Yes"])
    submit = st.form_submit_button("Check My Health")

if submit:
    if not symptoms.strip():
        st.warning("Please describe your symptoms.")
    else:
        with st.spinner("Analyzing your health inputs with AI..."):
            prompt = f"""
            You are a responsible AI health assistant. Provide non-diagnostic guidance based on the input:

            Age: {age}
            Gender: {gender}
            Location: {location}
            Symptom Duration: {duration}
            Symptoms: {symptoms}
            Medical History: {history}
            Medications: {medications}
            Lifestyle: {habits}

            1. List possible causes (based on symptoms)
            2. Suggest lifestyle or diet recommendations
            3. Indicate urgency level (Low, Medium, High)
            4. Recommend visiting a local doctor or clinic in {location}. Add friendly tone.

            Reminder: This is not a diagnosis.
            """

            # Call Together.ai API
            api_key = os.getenv("TOGETHER_API_KEY") or "your-together-api-key"
            endpoint = "https://api.together.xyz/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "mistralai/Mixtral-8x7b-Instruct-v0.1",
                "messages": [{"role": "user", "content": prompt}]
            }

            try:
                response = requests.post(endpoint, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                reply = result["choices"][0]["message"]["content"].strip()
                st.success("Here's what the AI suggests:")
                st.write(reply)

                # Suggest UAE clinics
                st.markdown("---")
                st.subheader(f"🏥 Known Clinics in {location}:")
                for clinic in uae_clinics.get(location, []):
                    st.write(f"✅ {clinic}")

            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("**Disclaimer:** This tool is for educational use only. Always consult a medical professional for serious concerns.")
