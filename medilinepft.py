import streamlit as st
import os
import requests

st.set_page_config(page_title="AI Health Checker", page_icon="🩺")
st.title("🩺 AI Health Checker")
st.markdown("This tool provides **AI-powered, non-diagnostic** health advice based on your symptoms.\n\n⚠️ This is not a substitute for professional medical advice.")

# Collect user input
with st.form("health_form"):
    age = st.number_input("Your Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    symptoms = st.text_area("Describe your symptoms")
    history = st.text_input("Any pre-existing conditions (e.g., diabetes, asthma)?")
    submit = st.form_submit_button("Check My Health")

if submit:
    if not symptoms.strip():
        st.warning("Please describe your symptoms.")
    else:
        with st.spinner("Analyzing your health inputs with AI..."):
            prompt = f"""
            Act as a responsible AI health assistant. Provide non-diagnostic guidance based on the input.

            Age: {age}
            Gender: {gender}
            Symptoms: {symptoms}
            Medical History: {history}

            Offer possible causes, lifestyle suggestions, and urgency level (Low, Medium, High).
            Add a friendly tone and recommend seeing a doctor if needed.
            """

            # Use Together.ai (proxy OpenRouter model) without login
            endpoint = "https://api.together.xyz/v1/chat/completions"
            api_key = os.getenv("TOGETHER_API_KEY") or "your-together-api-key"

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
            except Exception as e:
                st.error(f"Error: {e}")
