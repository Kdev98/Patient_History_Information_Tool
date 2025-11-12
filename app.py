import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Patient History Form",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .section-header {
        background-color: #e8f4f8;
        padding: 15px;
        border-left: 4px solid #1f77b4;
        margin-top: 20px;
        margin-bottom: 15px;
        border-radius: 5px;
    }
    .required-field {
        color: red;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Header
st.markdown("<h1 class='main-header'>🏥 Patient Medical History Form</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Please complete this form with as much detail as possible. Your information helps us provide better care.</p>", unsafe_allow_html=True)
st.divider()

# Create form
form = st.form(key="patient_form")

# ========== BASIC INFORMATION SECTION ==========
with form:
    st.markdown("<div class='section-header'><h2>📋 Basic Information</h2></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input(
            "Full Name *",
            placeholder="Enter your full name",
            help="Please provide your full name"
        )
    
    with col2:
        patient_dob = st.date_input(
            "Date of Birth *",
            value=None,
            help="Select your date of birth"
        )

    # ========== PRESENTING COMPLAINT SECTION ==========
    st.markdown("<div class='section-header'><h2>🔍 Chief Complaint</h2></div>", unsafe_allow_html=True)
    
    presenting_complaint = st.selectbox(
        "What is your main reason for visiting today? *",
        [
            "Select a complaint...",
            "Chest Pain",
            "Other"
        ],
        help="Please select your main complaint from the list"
    )

    # ========== HISTORY OF PRESENTING COMPLAINT ==========
    if presenting_complaint == "Chest Pain":
        st.markdown("<div class='section-header'><h2>💔 History of Chest Pain</h2></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            pain_start_date = st.date_input(
                "When did the pain start?",
                value=None,
                help="Select the date when the pain began"
            )
        
        with col2:
            pain_start_time = st.time_input(
                "What time did it start?",
                value=None,
                help="Select the time when the pain began (optional)"
            )
        
        pain_site = st.multiselect(
            "Where is the pain located? (Select all that apply)",
            [
                "Left side of chest",
                "Right side of chest",
                "Center of chest",
                "Upper chest",
                "Lower chest",
                "Back",
                "Not sure"
            ],
            help="Select the location(s) of your pain"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            pain_onset = st.radio(
                "How did the pain start?",
                ["Sudden", "Gradual"],
                help="Was the pain sudden or did it come on gradually?"
            )
        
        with col2:
            pain_character = st.multiselect(
                "What does the pain feel like?",
                [
                    "Throbbing/Pounding",
                    "Heavy/Pressure",
                    "Tight/Squeezing",
                    "Sharp/Stabbing",
                    "Burning",
                    "Dull/Aching",
                    "Not sure"
                ],
                help="Describe the character of your pain"
            )
        
        pain_radiation = st.multiselect(
            "Does the pain travel anywhere else? (Select all that apply)",
            [
                "Left arm",
                "Right arm",
                "Both arms",
                "Neck",
                "Jaw",
                "Back",
                "Shoulder",
                "No radiation"
            ],
            help="Select where the pain radiates to (if anywhere)"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            pain_timing = st.radio(
                "Is the pain constant or intermittent?",
                ["Constant", "Intermittent (comes and goes)"],
                help="Does the pain stay all the time or come and go?"
            )
        
        with col2:
            pain_severity = st.slider(
                "Pain Severity",
                min_value=0,
                max_value=10,
                value=5,
                help="0 = No pain | 10 = Worst pain of your life"
            )
            st.caption(f"You selected: {pain_severity}/10")
        
        pain_exacerbating = st.text_area(
            "What makes the pain worse? (If anything)",
            placeholder="e.g., Movement, breathing deeply, physical activity, lying down, etc.",
            height=80,
            help="Describe what makes your pain worse"
        )
        
        pain_relieving = st.text_area(
            "What makes the pain better? (If anything)",
            placeholder="e.g., Rest, medication, position changes, heat/cold, etc.",
            height=80,
            help="Describe what makes your pain better"
        )
    
    elif presenting_complaint == "Other":
        st.markdown("<div class='section-header'><h2>📝 History of Complaint</h2></div>", unsafe_allow_html=True)
        
        other_complaint_detail = st.text_area(
            "Please describe your complaint in detail:",
            placeholder="Describe when it started, how it developed, and any relevant details...",
            height=150,
            help="Provide as much detail as possible about your symptoms"
        )
    
    # ========== SYSTEMS REVIEW SECTION ==========
    st.markdown("<div class='section-header'><h2>🔬 Systems Review</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 14px; color: #666;'>Have you experienced any of the following?</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fever = st.checkbox("Fever")
        cough_cold = st.checkbox("Cough/Cold symptoms")
        unwell_contacts = st.checkbox("Contact with unwell people")
        sob = st.checkbox("Shortness of breath")
        calf_pain = st.checkbox("Calf pain")
    
    with col2:
        recent_surgery = st.checkbox("Recent surgery")
        travel_history = st.checkbox("Recent travel")
        haemoptysis = st.checkbox("Coughing up blood")
        malignancy_history = st.checkbox("History of cancer")
        prev_vte = st.checkbox("Previous blood clot (DVT/PE)")
    
    with col3:
        orthopnea = st.checkbox("Difficulty breathing when lying flat")
        abdominal_pain = st.checkbox("Abdominal pain")
        vomiting = st.checkbox("Vomiting")
        loss_consciousness = st.checkbox("Loss of consciousness")
        dizziness = st.checkbox("Dizziness")
    
    # ========== PAST MEDICAL HISTORY SECTION ==========
    st.markdown("<div class='section-header'><h2>📜 Past Medical History</h2></div>", unsafe_allow_html=True)
    
    pmh = st.text_area(
        "List any medical conditions you have had (e.g., diabetes, hypertension, heart disease, asthma, etc.):",
        placeholder="e.g., Type 2 Diabetes, High Blood Pressure, Asthma...",
        height=80,
        help="Include any significant past medical conditions"
    )
    
    # ========== DRUG HISTORY SECTION ==========
    st.markdown("<div class='section-header'><h2>💊 Current Medications</h2></div>", unsafe_allow_html=True)
    
    drug_history = st.text_area(
        "List any medications you currently take (include doses if you know them):",
        placeholder="e.g., Aspirin 100mg daily, Metformin 500mg twice daily...",
        height=80,
        help="Include medication name and dose if possible"
    )
    
    # ========== DRUG ALLERGIES SECTION ==========
    st.markdown("<div class='section-header'><h2>⚠️ Drug Allergies</h2></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        has_allergies = st.radio(
            "Do you have any drug allergies?",
            ["No", "Yes"],
            help="Select whether you have any known drug allergies"
        )
    
    if has_allergies == "Yes":
        with col2:
            drug_allergies = st.text_area(
                "Please list your drug allergies and reactions:",
                placeholder="e.g., Penicillin (rash), Aspirin (stomach upset)...",
                height=80,
                help="List the drug and the reaction you had"
            )
    else:
        drug_allergies = "No known drug allergies"
    
    # ========== FAMILY HISTORY SECTION ==========
    st.markdown("<div class='section-header'><h2>👨‍👩‍👧‍👦 Family History</h2></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        family_heart_attack = st.checkbox("Family history of heart attack")
    
    with col2:
        family_stroke = st.checkbox("Family history of stroke")
    
    family_history_detail = st.text_area(
        "Any other important family medical history?",
        placeholder="e.g., Who had the condition, at what age, etc.",
        height=80,
        help="Provide details about family members with medical conditions"
    )
    
    # ========== SOCIAL HISTORY SECTION ==========
    st.markdown("<div class='section-header'><h2>🚬 Social History</h2></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        smoking_status = st.radio(
            "Smoking status:",
            ["Never smoked", "Current smoker", "Ex-smoker"],
            help="Select your smoking status"
        )
    
    with col2:
        alcohol_use = st.radio(
            "Alcohol use:",
            ["None", "Occasional", "Regular", "Prefer not to say"],
            help="Select your alcohol consumption frequency"
        )
    
    recreational_drugs = st.radio(
        "Recreational drug use:",
        ["No", "Yes", "Prefer not to say"],
        help="Select whether you use recreational drugs"
    )
    
    if recreational_drugs == "Yes":
        recreational_drugs_detail = st.text_area(
            "Please specify:",
            placeholder="Type of drug and frequency of use...",
            height=80,
            help="Provide details about recreational drug use"
        )
    else:
        recreational_drugs_detail = ""
    
    # ========== ADDITIONAL INFORMATION SECTION ==========
    st.markdown("<div class='section-header'><h2>📝 Additional Information</h2></div>", unsafe_allow_html=True)
    
    additional_info = st.text_area(
        "Is there anything else you would like to tell the doctor?",
        placeholder="Any other relevant information about your health or current symptoms...",
        height=100,
        help="Add any other important information"
    )
    
    # ========== RECEIVING EMAIL SECTION ==========
    st.markdown("<div class='section-header'><h2>📧 Submit Form</h2></div>", unsafe_allow_html=True)
    
    receiving_email = st.text_input(
        "Receiving Email Address *",
        placeholder="doctor@clinic.com",
        help="Enter the email address where this form should be sent"
    )
    
    patient_email = st.text_input(
        "Your Email Address (optional)",
        placeholder="your.email@example.com",
        help="Enter your email address if you'd like a copy of your submission"
    )
    
    st.divider()
    
    # Submit button
    submitted = st.form_submit_button(
        "✅ Submit Form",
        use_container_width=True,
        type="primary"
    )
    
    # Form validation and submission
    if submitted:
        # Validation
        errors = []
        
        if not patient_name or patient_name.strip() == "":
            errors.append("Full name is required")
        
        if patient_dob is None:
            errors.append("Date of birth is required")
        
        if presenting_complaint == "Select a complaint...":
            errors.append("Please select a presenting complaint")
        
        if not receiving_email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', receiving_email):
            errors.append("Please enter a valid receiving email address")
        
        # Display errors
        if errors:
            st.error("❌ Please fix the following errors:")
            for error in errors:
                st.write(f"• {error}")
        else:
            # Prepare form data
            form_data = prepare_form_data(
                patient_name, patient_dob, presenting_complaint,
                pain_start_date if presenting_complaint == "Chest Pain" else None,
                pain_start_time if presenting_complaint == "Chest Pain" else None,
                pain_site if presenting_complaint == "Chest Pain" else None,
                pain_onset if presenting_complaint == "Chest Pain" else None,
                pain_character if presenting_complaint == "Chest Pain" else None,
                pain_radiation if presenting_complaint == "Chest Pain" else None,
                pain_timing if presenting_complaint == "Chest Pain" else None,
                pain_severity if presenting_complaint == "Chest Pain" else None,
                pain_exacerbating if presenting_complaint == "Chest Pain" else None,
                pain_relieving if presenting_complaint == "Chest Pain" else None,
                other_complaint_detail if presenting_complaint == "Other" else None,
                fever, cough_cold, unwell_contacts, sob, calf_pain, recent_surgery,
                travel_history, haemoptysis, malignancy_history, prev_vte, orthopnea,
                abdominal_pain, vomiting, loss_consciousness, dizziness,
                pmh, drug_history, drug_allergies, family_heart_attack, family_stroke,
                family_history_detail, smoking_status, alcohol_use, recreational_drugs,
                recreational_drugs_detail, additional_info
            )
            
            # Try to send email
            with st.spinner("Sending form..."):
                if send_email(receiving_email, form_data, patient_email):
                    st.session_state.form_submitted = True
                    st.success("✅ Form submitted successfully!")
                    st.balloons()
                    st.info(f"Your form has been sent to: {receiving_email}")
                else:
                    st.error("❌ Error sending form. Please check email configuration.")


def prepare_form_data(patient_name, patient_dob, presenting_complaint,
                     pain_start_date, pain_start_time, pain_site, pain_onset,
                     pain_character, pain_radiation, pain_timing, pain_severity,
                     pain_exacerbating, pain_relieving, other_complaint_detail,
                     fever, cough_cold, unwell_contacts, sob, calf_pain, recent_surgery,
                     travel_history, haemoptysis, malignancy_history, prev_vte, orthopnea,
                     abdominal_pain, vomiting, loss_consciousness, dizziness,
                     pmh, drug_history, drug_allergies, family_heart_attack, family_stroke,
                     family_history_detail, smoking_status, alcohol_use, recreational_drugs,
                     recreational_drugs_detail, additional_info):
    """Prepare form data as formatted HTML"""
    
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .section { margin: 20px 0; padding: 15px; border-left: 4px solid #1f77b4; background-color: #f9f9f9; }
            .section h2 { color: #1f77b4; margin-top: 0; }
            .field { margin: 10px 0; }
            .label { font-weight: bold; color: #1f77b4; }
            .value { margin-left: 10px; }
            hr { border: none; border-top: 2px solid #1f77b4; margin: 30px 0; }
        </style>
    </head>
    <body>
        <h1>Patient Medical History Form</h1>
        <p>Submitted: {timestamp}</p>
        <hr>
        
        <div class="section">
            <h2>Basic Information</h2>
            <div class="field">
                <span class="label">Name:</span>
                <span class="value">{patient_name}</span>
            </div>
            <div class="field">
                <span class="label">Date of Birth:</span>
                <span class="value">{patient_dob}</span>
            </div>
        </div>
        
        <div class="section">
            <h2>Chief Complaint</h2>
            <div class="field">
                <span class="label">Presenting Complaint:</span>
                <span class="value">{presenting_complaint}</span>
            </div>
        </div>
        
        {hpc_section}
        
        <div class="section">
            <h2>Systems Review</h2>
            <div class="field">
                <span class="label">Fever:</span>
                <span class="value">{'Yes' if fever else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Cough/Cold Symptoms:</span>
                <span class="value">{'Yes' if cough_cold else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Unwell Contacts:</span>
                <span class="value">{'Yes' if unwell_contacts else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Shortness of Breath:</span>
                <span class="value">{'Yes' if sob else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Calf Pain:</span>
                <span class="value">{'Yes' if calf_pain else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Recent Surgery:</span>
                <span class="value">{'Yes' if recent_surgery else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Recent Travel:</span>
                <span class="value">{'Yes' if travel_history else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Haemoptysis (Coughing up blood):</span>
                <span class="value">{'Yes' if haemoptysis else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">History of Cancer:</span>
                <span class="value">{'Yes' if malignancy_history else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Previous Blood Clot (DVT/PE):</span>
                <span class="value">{'Yes' if prev_vte else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Difficulty Breathing When Lying Flat:</span>
                <span class="value">{'Yes' if orthopnea else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Abdominal Pain:</span>
                <span class="value">{'Yes' if abdominal_pain else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Vomiting:</span>
                <span class="value">{'Yes' if vomiting else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Loss of Consciousness:</span>
                <span class="value">{'Yes' if loss_consciousness else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Dizziness:</span>
                <span class="value">{'Yes' if dizziness else 'No'}</span>
            </div>
        </div>
        
        <div class="section">
            <h2>Past Medical History</h2>
            <div class="field">
                <span class="value">{pmh if pmh else 'None reported'}</span>
            </div>
        </div>
        
        <div class="section">
            <h2>Current Medications</h2>
            <div class="field">
                <span class="value">{drug_history if drug_history else 'None reported'}</span>
            </div>
        </div>
        
        <div class="section">
            <h2>Drug Allergies</h2>
            <div class="field">
                <span class="value">{drug_allergies}</span>
            </div>
        </div>
        
        <div class="section">
            <h2>Family History</h2>
            <div class="field">
                <span class="label">Family History of Heart Attack:</span>
                <span class="value">{'Yes' if family_heart_attack else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Family History of Stroke:</span>
                <span class="value">{'Yes' if family_stroke else 'No'}</span>
            </div>
            <div class="field">
                <span class="label">Additional Family History:</span>
                <span class="value">{family_history_detail if family_history_detail else 'None reported'}</span>
            </div>
        </div>
        
        <div class="section">
            <h2>Social History</h2>
            <div class="field">
                <span class="label">Smoking Status:</span>
                <span class="value">{smoking_status}</span>
            </div>
            <div class="field">
                <span class="label">Alcohol Use:</span>
                <span class="value">{alcohol_use}</span>
            </div>
            <div class="field">
                <span class="label">Recreational Drug Use:</span>
                <span class="value">{recreational_drugs}</span>
            </div>
            {recreational_drugs_detail_section}
        </div>
        
        <div class="section">
            <h2>Additional Information</h2>
            <div class="field">
                <span class="value">{additional_info if additional_info else 'None provided'}</span>
            </div>
        </div>
        
        <hr>
        <p style="font-size: 12px; color: #666; text-align: center;">
            This form was generated automatically by the Patient History Information Tool.
        </p>
    </body>
    </html>
    """
    
    # Build HPC section based on complaint type
    if presenting_complaint == "Chest Pain":
        hpc_section = f"""
        <div class="section">
            <h2>History of Chest Pain</h2>
            <div class="field">
                <span class="label">When did the pain start:</span>
                <span class="value">{pain_start_date if pain_start_date else 'Not specified'} {f'at {pain_start_time}' if pain_start_time else ''}</span>
            </div>
            <div class="field">
                <span class="label">Site of Pain:</span>
                <span class="value">{', '.join(pain_site) if pain_site else 'Not specified'}</span>
            </div>
            <div class="field">
                <span class="label">Onset:</span>
                <span class="value">{pain_onset if pain_onset else 'Not specified'}</span>
            </div>
            <div class="field">
                <span class="label">Character of Pain:</span>
                <span class="value">{', '.join(pain_character) if pain_character else 'Not specified'}</span>
            </div>
            <div class="field">
                <span class="label">Radiation:</span>
                <span class="value">{', '.join(pain_radiation) if pain_radiation else 'No radiation'}</span>
            </div>
            <div class="field">
                <span class="label">Timing:</span>
                <span class="value">{pain_timing if pain_timing else 'Not specified'}</span>
            </div>
            <div class="field">
                <span class="label">Severity (0-10):</span>
                <span class="value">{pain_severity}/10</span>
            </div>
            <div class="field">
                <span class="label">Exacerbating Factors:</span>
                <span class="value">{pain_exacerbating if pain_exacerbating else 'None reported'}</span>
            </div>
            <div class="field">
                <span class="label">Relieving Factors:</span>
                <span class="value">{pain_relieving if pain_relieving else 'None reported'}</span>
            </div>
        </div>
        """
    else:
        hpc_section = f"""
        <div class="section">
            <h2>History of Complaint</h2>
            <div class="field">
                <span class="value">{other_complaint_detail if other_complaint_detail else 'No details provided'}</span>
            </div>
        </div>
        """
    
    recreational_drugs_detail_section = ""
    if recreational_drugs == "Yes" and recreational_drugs_detail:
        recreational_drugs_detail_section = f"""
            <div class="field">
                <span class="label">Recreational Drug Details:</span>
                <span class="value">{recreational_drugs_detail}</span>
            </div>
        """
    
    html_content = html_content.format(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        patient_name=patient_name,
        patient_dob=patient_dob,
        presenting_complaint=presenting_complaint,
        hpc_section=hpc_section,
        fever=fever,
        cough_cold=cough_cold,
        unwell_contacts=unwell_contacts,
        sob=sob,
        calf_pain=calf_pain,
        recent_surgery=recent_surgery,
        travel_history=travel_history,
        haemoptysis=haemoptysis,
        malignancy_history=malignancy_history,
        prev_vte=prev_vte,
        orthopnea=orthopnea,
        abdominal_pain=abdominal_pain,
        vomiting=vomiting,
        loss_consciousness=loss_consciousness,
        dizziness=dizziness,
        pmh=pmh,
        drug_history=drug_history,
        drug_allergies=drug_allergies,
        family_heart_attack=family_heart_attack,
        family_stroke=family_stroke,
        family_history_detail=family_history_detail,
        smoking_status=smoking_status,
        alcohol_use=alcohol_use,
        recreational_drugs=recreational_drugs,
        recreational_drugs_detail_section=recreational_drugs_detail_section,
        additional_info=additional_info
    )
    
    return html_content


def send_email(receiving_email, form_data, patient_email=None):
    """Send form data via email"""
    try:
        # Email configuration - Update these with your email settings
        sender_email = st.secrets.get("SENDER_EMAIL", "")
        sender_password = st.secrets.get("SENDER_PASSWORD", "")
        smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = st.secrets.get("SMTP_PORT", 587)
        
        # Check if email configuration is available
        if not sender_email or not sender_password:
            st.error("Email configuration not found. Please set up email credentials in secrets.")
            st.info("To set up email, add SENDER_EMAIL, SENDER_PASSWORD, SMTP_SERVER, and SMTP_PORT to .streamlit/secrets.toml")
            return False
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Patient Medical History Form Submission"
        message["From"] = sender_email
        message["To"] = receiving_email
        
        # Attach HTML content
        part = MIMEText(form_data, "html")
        message.attach(part)
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiving_email, message.as_string())
        
        # Send copy to patient if requested
        if patient_email and patient_email.strip() != "":
            message_copy = MIMEMultipart("alternative")
            message_copy["Subject"] = "Your Patient Medical History Form - Copy"
            message_copy["From"] = sender_email
            message_copy["To"] = patient_email
            
            part_copy = MIMEText(form_data, "html")
            message_copy.attach(part_copy)
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, patient_email, message_copy.as_string())
        
        return True
    
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False
