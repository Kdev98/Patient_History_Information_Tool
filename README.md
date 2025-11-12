# 🏥 Patient History Information Tool

A user-friendly Streamlit application that allows patients to fill in their medical history form while waiting in the waiting room. The completed form is automatically sent via email to the clinic/doctor for review before the appointment.

## Features

✅ **Easy-to-Use Interface** - Intuitive form design for non-medical users
✅ **Comprehensive Medical History** - Captures all essential patient information
✅ **Chest Pain Specific Questions** - Detailed questions for chest pain complaints
✅ **Systems Review** - Systematic review of all major body systems
✅ **Email Integration** - Automatically sends completed forms to clinic email
✅ **Patient Copy** - Optional copy sent to patient's email
✅ **Form Validation** - Ensures all required fields are completed
✅ **Responsive Design** - Works on desktop, tablet, and mobile devices

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Repository
```bash
cd Patient_History_Information_Tool
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Email Settings

#### Option A: Using Gmail (Recommended)

1. **Enable 2-Factor Authentication**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification if you haven't already

2. **Create an App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or your device)
   - Google will generate a 16-character password
   - Copy this password

3. **Update `.streamlit/secrets.toml`**
   ```toml
   SENDER_EMAIL = "your-email@gmail.com"
   SENDER_PASSWORD = "your-16-char-app-password"
   SMTP_SERVER = "smtp.gmail.com"
   SMTP_PORT = 587
   ```

#### Option B: Using Other Email Providers

**Outlook/Office365:**
```toml
SENDER_EMAIL = "your-email@outlook.com"
SENDER_PASSWORD = "your-password"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
```

**Yahoo Mail:**
```toml
SENDER_EMAIL = "your-email@yahoo.com"
SENDER_PASSWORD = "your-app-password"
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
```

### Step 5: Run the Application
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

### For Patients
1. Open the application on a waiting room computer/tablet
2. Fill in your personal information
3. Select your main complaint from the dropdown
4. Answer detailed questions about your symptoms
5. Complete all other sections (medical history, medications, allergies, etc.)
6. Enter the clinic's email address
7. Optionally enter your own email to receive a copy
8. Click "Submit Form"
9. The form will be sent to the clinic via email

### For Healthcare Providers
1. Patients can access the app from the waiting room
2. Review submitted forms in your email inbox
3. Confirm or update information during the patient consultation
4. This saves valuable appointment time!

## Form Sections

### 📋 Basic Information
- Full Name
- Date of Birth

### 🔍 Chief Complaint
- Presenting Complaint (dropdown menu)
- Currently includes: Chest Pain, Other

### 💔 History of Presenting Complaint
For chest pain, the form collects:
- When pain started (date and time)
- Location of pain (multiselect)
- Onset (sudden vs gradual)
- Character of pain (throbbing, heavy, tight, etc.)
- Radiation (arms, neck, jaw, back, etc.)
- Timing (constant vs intermittent)
- Severity (0-10 pain scale)
- Exacerbating factors
- Relieving factors

### 🔬 Systems Review
Checks for:
- Fever
- Cough/Cold symptoms
- Contact with unwell people
- Shortness of breath
- Calf pain
- Recent surgery
- Recent travel
- Coughing up blood
- History of cancer
- Previous blood clots
- Difficulty breathing when lying down
- Abdominal pain
- Vomiting
- Loss of consciousness
- Dizziness

### 📜 Past Medical History
- Free text field for patient to list previous conditions

### 💊 Current Medications
- Free text field to list current medications with doses

### ⚠️ Drug Allergies
- Yes/No option
- Free text field for specific allergies and reactions

### 👨‍👩‍👧‍👦 Family History
- Family history of heart attack
- Family history of stroke
- Additional family medical history

### 🚬 Social History
- Smoking status
- Alcohol use
- Recreational drug use

### 📝 Additional Information
- Any other relevant information the patient wants to share

## Customization

### Adding More Presenting Complaints

Edit `app.py` and find the "Chief Complaint" section. Add your complaint to the dropdown:

```python
presenting_complaint = st.selectbox(
    "What is your main reason for visiting today? *",
    [
        "Select a complaint...",
        "Chest Pain",
        "Shortness of Breath",  # Add new complaint
        "Other"
    ]
)
```

Then add a corresponding section in the history questions using `if presenting_complaint == "Your Complaint":` blocks.

### Changing Colors and Styling

Modify the CSS in the main section:

```python
st.markdown("""
    <style>
    .section-header {
        background-color: #e8f4f8;  # Change this color
        ...
    }
    </style>
    """, unsafe_allow_html=True)
```

### Changing the Receiving Email

The receiving email is entered by the user in the form. However, you can set a default:

Find this line:
```python
receiving_email = st.text_input(
    "Receiving Email Address *",
    placeholder="doctor@clinic.com",
```

Change to:
```python
receiving_email = st.text_input(
    "Receiving Email Address *",
    value="default-clinic@example.com",  # Add this
```

## Troubleshooting

### "Email configuration not found" Error
- Make sure you've updated `.streamlit/secrets.toml` with your email credentials
- Verify the file exists in the `.streamlit` folder

### "Login failed" or Authentication Error
- For Gmail: Make sure you're using an App Password (not your regular Gmail password)
- Verify 2-Factor Authentication is enabled on your email account
- Check that credentials in `secrets.toml` are correct

### Form not sending
- Check your internet connection
- Verify email configuration in `secrets.toml`
- Check that the receiving email address is valid
- Look for error messages in the Streamlit terminal

### Application won't start
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Try deactivating and reactivating your virtual environment
- Delete the `.streamlit` cache folder and try again: `rm -rf .streamlit/cache`

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit `secrets.toml` to version control** - This file contains sensitive credentials
2. **Use App Passwords** - Don't use your actual email password
3. **Restrict Access** - Only deploy to trusted networks (e.g., clinic's internal network)
4. **HTTPS** - For production use, deploy behind HTTPS
5. **Data Privacy** - Ensure compliance with HIPAA, GDPR, or local data protection regulations

## File Structure

```
Patient_History_Information_Tool/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── secrets.toml               # Email configuration (keep private!)
└── README.md                       # This file
```

## Future Enhancements

- [ ] Add database to store patient responses
- [ ] Add PDF export functionality
- [ ] Support for multiple complaint types
- [ ] Integration with EHR systems
- [ ] Patient authentication
- [ ] Form templates for different specialties
- [ ] Multi-language support
- [ ] Mobile app version

## License

This project is provided as-is for medical use. Ensure compliance with local regulations.

## Support

For issues or questions, please check:
1. The troubleshooting section above
2. Streamlit documentation: https://docs.streamlit.io
3. Python email documentation: https://docs.python.org/3/library/email.html

## Disclaimer

This application is designed to assist with patient intake and should not replace proper medical documentation procedures. Healthcare providers should maintain their own compliance and record-keeping standards.

---

**Built with ❤️ for healthcare professionals and their patients**
