### AI Health Checker - Streamlit App
# app.py

import streamlit as st
import os
import requests

st.set_page_config(page_title="AI Health Checker", page_icon="🩺")

st.title("🩺 AI Health Checker")
st.markdown("This tool provides **AI-powered, non-diagnostic** health advice based on your symptoms.\n\n⚠️ This is not a substitute for professional medical advice.")

# Collect user inputs
with st.form("health_form"):
    age = st.number_input("Your Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    symptoms = st.text_area("Describe your symptoms")
    history = st.text_input("Any pre-existing conditions (e.g., diabetes, asthma)?")
    submit = st.form_submit_button("Check My Health")

# Handle form submission
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

            # Set OpenRouter or Groq API key and endpoint
            api_key = os.getenv("OPENROUTER_API_KEY") or "your-openrouter-key"
            endpoint = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "openai/gpt-3.5-turbo",  # or try "mistralai/mixtral-8x7b" for free use
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }

            try:
                response = requests.post(endpoint, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                reply = result["choices"][0]["message"]["content"].strip()
                st.success("Here's what the AI suggests:")
                st.write(reply)

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Disclaimer:** This tool is for educational use only. Always consult a medical professional for serious concerns.")