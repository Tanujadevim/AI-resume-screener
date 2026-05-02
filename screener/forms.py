from django import forms

class ResumeForm(forms.Form):
    resume_file = forms.FileField(
        label="Upload Your Resume (PDF)",
        help_text="Only PDF files Please"
    )
    job_description = forms.CharField(
        label="Paste Job Description Here",
        widget=forms.Textarea(attrs={
            'rows': 8,
            'placeholder': "Copy and paste the full job description here..."
        })
    )