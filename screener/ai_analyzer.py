import os
from groq import Groq
import pdfplumber
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if not text.strip():
            print("Text extraction failed, trying OCR...")
            try:
                from pdf2image import convert_from_bytes
                import io

                # Handle both BytesIO and file objects
                if hasattr(pdf_file, 'read'):
                    pdf_file.seek(0)
                    pdf_bytes = pdf_file.read()
                else:
                    pdf_bytes = pdf_file

                images = convert_from_bytes(
                    pdf_bytes,
                    dpi=300,
                    poppler_path=r'C:\poppler-25.12.0\Library\bin'
                )
                for img in images:
                    text += pytesseract.image_to_string(img) + "\n"

                print(f"OCR extracted {len(text)} characters")
            except Exception as ocr_error:
                print(f"OCR failed: {ocr_error}")

        print(f"Final text length: {len(text)}")
        print(f"Preview: {text[:200]}")
        return text.strip()

    except Exception as e:
        print(f"PDF extraction error: {e}")
        return ""


def analyze_resume(resume_text, job_description):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are a strict resume screening AI. Your job is to compare a resume against a job description HONESTLY.

ABSOLUTE RULES:
1. NEVER mention a skill in STRENGTHS unless it appears in the resume text
2. Partial matches count — if resume has Python and JD wants Python + Java, that is a partial match, not zero
3. A completely unrelated resume should score 10-30 maximum
4. Be fair — a Python resume vs Python JD should score 50-80 depending on specific matches

RESUME TEXT:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION:
\"\"\"
{job_description}
\"\"\"

Respond in EXACTLY this format:

SCORE: [number between 0 and 100]

STRENGTHS:
- [only real skills from resume that match JD]
- [only real skills from resume that match JD]
- [only real skills from resume that match JD]

GAPS:
- [skill in JD completely missing from resume]
- [skill in JD completely missing from resume]
- [skill in JD completely missing from resume]

TIP:
[one specific actionable tip]
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a strict honest resume screener. You NEVER invent skills. You ONLY report what is literally written in the resume text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content