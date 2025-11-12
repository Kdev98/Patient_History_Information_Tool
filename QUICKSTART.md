# Quick Start Guide - Patient History Information Tool

## 🚀 Get Started in 5 Minutes

### Step 1: Set Up Python Environment
```bash
cd Patient_History_Information_Tool
python -m venv venv
venv\Scripts\activate  # On Windows
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Email (Important!)

**For Gmail Users:**
1. Go to https://myaccount.google.com/apppasswords
2. Copy your 16-character App Password
3. Open `.streamlit/secrets.toml` and paste:
   ```
   SENDER_EMAIL = "your-email@gmail.com"
   SENDER_PASSWORD = "your-16-char-password"
   SMTP_SERVER = "smtp.gmail.com"
   SMTP_PORT = 587
   ```

### Step 4: Run the App
```bash
streamlit run app.py
```

That's it! 🎉 The app will open at `http://localhost:8501`

## 📝 What to Do Next

1. **Test the form** - Fill it out to make sure everything works
2. **Customize** - Edit the form if needed
3. **Deploy** - See README.md for deployment options

## ❓ Common Issues

**"Email configuration not found"**
→ Update `.streamlit/secrets.toml` with your email credentials

**"Login failed"**
→ For Gmail, use an App Password (not your regular password)

**"Port 8501 already in use"**
```bash
streamlit run app.py --logger.level=debug --server.port 8502
```

## 📚 Learn More

- Full documentation: See `README.md`
- Streamlit docs: https://docs.streamlit.io
- Gmail App Passwords: https://support.google.com/accounts/answer/185833

---

Need help? Check the README.md file or email configuration section!
