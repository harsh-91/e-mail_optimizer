# 📬 Email Delivery Optimizer

A unified email deliverability and diagnostics tool with a Web UI, Desktop GUI, and CLI.

It helps you:
- ✅ Check domain SPF, DKIM, and DMARC records
- ✅ Compose and send authenticated travel quote emails
- ✅ Receive and analyze real email headers for authentication results

---

## 🔧 Features

| Feature                  | Description |
|--------------------------|-------------|
| ✅ SPF/DKIM/DMARC Checker | Verify your domain’s DNS setup |
| ✅ Email Sender           | Send structured emails using Gmail + App Password |
| ✅ Header Analyzer        | Parse and explain inbound email headers |
| 💻 GUI (Tkinter)          | Desktop version for non-technical users |
| 🧪 CLI Tool               | Terminal-based utility (optional) |

---

## 🚀 Getting Started

### 1. Clone & Enter Project
```bash
git clone https://github.com/yourusername/email-delivery-optimizer.git
cd email-delivery-optimizer

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\activate

3. Install Requirements
pip install -r requirements.txt

4. Add Gmail Credentials
# config/.env
GMAIL_USER=yourname@gmail.com
GMAIL_APP_PASSWORD=your16charapppassword

Web App
Start the Flask Server
python run.py

Access it at:
http://localhost:5000

Web Features:
Route	Functionality
/	Enter a domain and DKIM selector to check SPF, DKIM, DMARC
/email	Send authenticated HTML emails via Gmail
/analyze	Analyze headers of recent inbound emails to your inbox

💻 Desktop GUI (Tkinter)
python gui/gui_app.py
This opens a local desktop app:
 Runs the same checks
 Composes + sends emails
 Built-in help & instruction blocks

🔍 Inbound Email Header Analysis
 Users can send a test email to your Gmail address, and the app will:

🔍 Parse headers like Received-SPF, Authentication-Results, and DKIM-Signature

✅ Show pass/fail results

💡 Explain what each part means (SPF, DKIM, DMARC)

📌 Recommend fixes (coming soon)

Uses IMAPClient + pyzmail36 to securely fetch and parse Gmail headers

📂 Project Structure Overview

.
├── app/            # Flask UI (routes, templates)
├── core/           # Core logic: diagnostics, formatting, parsing
├── gui/            # Desktop GUI with Tkinter
├── config/         # .env for credentials
├── static/         # CSS styling
├── run.py          # Flask entrypoint
├── main.py         # CLI (optional)
├── requirements.txt
└── README.md

🛡️ Security Notes
  App Passwords are not stored, only used in memory

.env is ignored via .gitignore

You can remove .env entirely if using web inputs only

🧠 Glossary
 SPF: Validates the mail server is allowed to send for the domain
 DKIM: Ensures the message is signed with a domain-specific key
 DMARC: Combines SPF + DKIM to instruct mailbox providers on enforcement
 App Password: A special Google password (required if 2FA is on) used instead of your main password
     Generate one here → https://myaccount.google.com/apppasswords

Future Enhancements
 Export audit reports as PDF or HTML
 Auto suggestions for DNS fixes
 Dark mode + mobile styling
 Mailgun/Postfix support for enterprise setups
 Deployment to Railway or Render

🧑‍💻 Author & License
MIT License © 2025 Harsh-91
Feel free to fork, enhance, or use commercially — with credit.
