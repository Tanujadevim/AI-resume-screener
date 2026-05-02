import io
from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import ResumeSubmission
from .ai_analyzer import extract_text_from_pdf, analyze_resume

def home(request):
    form = ResumeForm()

    if request.method == 'POST':
        print("--- POST received ---")
        
        resume_text = request.POST.get('resume_text', '').strip()
        job_description = request.POST.get('job_description', '').strip()
        
        if not job_description:
            return render(request, 'screener/home.html', {
                'form': form,
                'error': 'Please paste a job description.'
            })

        # Try to get resume text from uploaded file
        if not resume_text:
            form = ResumeForm(request.POST, request.FILES)
            if form.is_valid():
                resume_file = form.cleaned_data['resume_file']
                try:
                    file_bytes = resume_file.read()
                    file_obj = io.BytesIO(file_bytes)
                    resume_text = extract_text_from_pdf(file_obj)
                    resume_file.seek(0)
                except Exception as e:
                    print(f"PDF read error: {e}")
            else:
                # Try saved resume from DB
                try:
                    last = ResumeSubmission.objects.order_by('-submitted_at').first()
                    if last and last.resume_file:
                        with open(last.resume_file.path, 'rb') as f:
                            file_obj = io.BytesIO(f.read())
                            resume_text = extract_text_from_pdf(file_obj)
                except Exception as e:
                    print(f"Saved resume error: {e}")

        if not resume_text:
            return render(request, 'screener/home.html', {
                'form': ResumeForm(),
                'show_paste_box': True,
                'error': 'Could not read your PDF. Please paste your resume text below.'
            })

        try:
            ai_result = analyze_resume(resume_text, job_description)
            
            # Save submission
            resume_file = request.FILES.get('resume_file')
            submission = ResumeSubmission(
                job_description=job_description,
                feedback=ai_result,
            )
            if resume_file:
                submission.resume_file = resume_file
            submission.save()
            
            return redirect('result', pk=submission.id)

        except Exception as e:
            print(f"--- ERROR: {e} ---")
            return render(request, 'screener/home.html', {
                'form': ResumeForm(),
                'error': str(e)
            })

    return render(request, 'screener/home.html', {'form': form})


def result(request, pk):
    submission = ResumeSubmission.objects.get(id=pk)
    return render(request, 'screener/result.html', {'submission': submission})