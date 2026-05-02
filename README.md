# 🧠 AI Resume Screener

> Upload your resume, paste a job description — get an instant AI-powered match score with strengths, gaps, and actionable tips.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-5.2-green?style=flat-square&logo=django)
![Groq](https://img.shields.io/badge/AI-Groq%20LLaMA%203-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

---

## 🚀 Live Demo

🔗 **[Coming Soon — Deploying on Railway](#)**

---

## 📸 Screenshots

| Home Page | Result Page |
|-----------|-------------|
| Upload resume + paste JD | AI score, strengths, gaps & tip |

---

## ✨ Features

- 📄 **PDF Resume Upload** — supports both text-based and image-based PDFs
- 🔍 **OCR Support** — reads image PDFs using Tesseract OCR automatically
- 🤖 **AI-Powered Analysis** — uses Groq's LLaMA 3.3 70B model for accurate matching
- 📊 **Match Score** — 0–100 score with verdict (Poor / Moderate / Strong / Excellent)
- 💪 **Strengths** — skills from your resume that match the job
- 🚧 **Gaps** — skills required in the JD but missing from your resume
- 💡 **Actionable Tip** — one specific improvement suggestion per analysis
- 🗄️ **Database Storage** — all submissions saved with timestamps
- 📱 **Clean Responsive UI** — works on desktop and mobile

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Django 5.2 |
| AI / LLM | Groq API (LLaMA 3.3 70B) |
| PDF Reading | pdfplumber + PyPDF2 |
| OCR | Tesseract OCR + pdf2image |
| Database | SQLite (dev) |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Railway |

---

## ⚙️ How It Works

```
User uploads PDF resume
        ↓
pdfplumber tries text extraction
        ↓
If empty → Tesseract OCR reads the image PDF
        ↓
Resume text + Job Description sent to Groq AI
        ↓
LLaMA 3.3 analyzes and returns structured response
        ↓
Score, Strengths, Gaps, Tip displayed beautifully
```

---

## 🏃 Run Locally

### Prerequisites
- Python 3.11+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed
- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) installed (Windows)
- [Groq API Key](https://console.groq.com) (free)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Tanujadevim/AI-resume-screener.git
cd AI-resume-screener

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
echo GROQ_API_KEY=your_groq_api_key_here > .env

# 5. Run migrations
python manage.py migrate

# 6. Start the server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

---

## 📁 Project Structure

```
AI-resume-screener/
├── core/                   # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── screener/               # Main app
│   ├── templates/
│   │   └── screener/
│   │       ├── home.html   # Upload form
│   │       └── result.html # AI analysis result
│   ├── ai_analyzer.py      # PDF extraction + Groq AI logic
│   ├── forms.py            # Django form
│   ├── models.py           # Database model
│   ├── urls.py             # URL routes
│   └── views.py            # Request handling logic
├── .env                    # Secret keys (not in repo)
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 🎯 Why I Built This

As a Python developer actively job hunting, I noticed that tailoring resumes for each job description is time-consuming and guesswork-heavy. This tool automates that process — giving instant, honest feedback on how well a resume matches a specific role, powered by a real LLM.

**Key learning outcomes from this project:**
- Django MVT architecture (Models, Views, Templates)
- File upload handling + PDF text extraction
- OCR pipeline for image-based PDFs
- LLM prompt engineering for structured outputs
- REST-style URL routing and form validation
- Database design and Django ORM

---

## 🙋‍♀️ About the Developer

**Tanuja Devi Muthayalapalli**
Python Developer | AI & Automation Enthusiast

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/tanuja-devi-muthayalapalli)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/Tanujadevim)
[![Medium](https://img.shields.io/badge/Medium-Read-black?style=flat-square&logo=medium)](https://medium.com/@Tanu_Writes)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">Built with 💙 by Tanuja Devi | 2025</p>
