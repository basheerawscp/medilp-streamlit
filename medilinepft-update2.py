### AI Health Checker - Streamlit App (PDF Report + Email Support)
# app.py

import streamlit as st
import os
import requests
import smtplib
from email.message import EmailMessage
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import datetime

st.set_page_config(page_title="AI Health Checker", page_icon="🩺")

st.title("🩺 AI Health Checker")
st.markdown("This tool provides **AI-powered, non-diagnostic** health advice based on your symptoms.\n\n⚠️ This is not a substitute for professional medical advice.")

# UAE clinic mapping (basic version)
uae_clinics = {
    "Dubai": ["Aster Clinic – Al Nahda", "Mediclinic – Dubai Mall", "NMC Specialty Hospital – Deira"],
    "Abu Dhabi": ["Burjeel Hospital", "NMC Royal – Khalifa City", "LLH Hospital – Musaffah"],
    "Sharjah": ["Thumbay Hospital", "Zulekha Hospital", "Al Zahra Hospital"]
}

# Function to create PDF report
def generate_pdf(user_data, ai_response):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    width, height = A4
    y = height - 50

    p.drawString(50, y, f"AI Health Report - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30

    for label, value in user_data.items():
        p.drawString(50, y, f"{label}: {value}")
        y -= 20

    y -= 10
    p.drawString(50, y, "AI Response:")
    y -= 20

    wrapped_lines = simpleSplit(ai_response, 'Helvetica', 12, width - 100)
    for line in wrapped_lines:
        p.drawString(60, y, line)
        y -= 15
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 50

    p.save()
    buffer.seek(0)
    return buffer

# Function to send email with attachment
def send_email(to_email, pdf_data):
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg['Subject'] = 'Your AI Health Checker Report'
    msg['From'] = email_address
    msg['To'] = to_email
    msg.set_content('Attached is your AI Health Report. Stay healthy!')

    msg.add_attachment(pdf_data.read(), maintype='application', subtype='pdf', filename='AI_Health_Report.pdf')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
            return True
    except Exception as e:
        st.error(f"Email failed: {e}")
        return False

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
    email_input = st.text_input("Enter your email to receive report (optional)")
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

            api_key = os.getenv("TOGETHER_API_KEY")
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

                st.subheader(f"🏥 Known Clinics in {location}:")
                for clinic in uae_clinics.get(location, []):
                    st.write(f"✅ {clinic}")

                # Generate PDF
                user_data = {
                    "Age": age,
                    "Gender": gender,
                    "Location": location,
                    "Symptom Duration": duration,
                    "Symptoms": symptoms,
                    "Medical History": history,
                    "Medications": medications,
                    "Lifestyle": habits,
                }
                pdf_buffer = generate_pdf(user_data, reply)
                st.download_button("📄 Download Health Report as PDF", pdf_buffer, file_name="AI_Health_Report.pdf")

                # Send Email if provided
                if email_input:
                    sent = send_email(email_input, pdf_buffer)
                    if sent:
                        st.success(f"📧 Report sent to {email_input}!")

            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown("**Disclaimer:** This tool is for educational use only. Always consult a medical professional for serious concerns.")
