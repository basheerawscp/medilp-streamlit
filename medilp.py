### AI Health Checker - Streamlit App
# app.py

# Note: This code requires the 'streamlit' and 'openai' modules.
# To install them, run: pip install streamlit openai

import os

st = None
OpenAIClient = None

try:
    import streamlit as st
except ImportError:
    print("Warning: Streamlit is not installed. Please install it using 'pip install streamlit'.")

try:
    from openai import OpenAI
    OpenAIClient = OpenAI
except ImportError:
    print("Warning: OpenAI module is not installed. Please install it using 'pip install openai'.")

if st is not None and OpenAIClient is not None:
    # Initialize OpenAI client
    client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY")

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

                try:
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}]
                    )

                    st.success("Here's what the AI suggests:")
                    st.write(response.choices[0].message.content.strip())

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown("**Disclaimer:** This tool is for educational use only. Always consult a medical professional for serious concerns.")

else:
    print("\nThe application requires both 'streamlit' and 'openai' modules to run.")
    print("Please make sure to install them in your environment:")
    print("  pip install streamlit openai")
