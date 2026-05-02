import os
from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import ResumeSubmission
from .ai_analyzer import extract_text_from_pdf, analyze_resume

def home(request):
    form = ResumeForm()

    if request.method == 'POST':
        print("--- POST received ---")
        using_saved = request.POST.get('using_saved') == 'true'

        if using_saved:
            last = ResumeSubmission.objects.order_by('-submitted_at').first()
            if last and last.resume_file:
                job_description = request.POST.get('job_description', '').strip()
                resume_text = request.POST.get('resume_text', '').strip()

                if not job_description:
                    return render(request, 'screener/home.html', {
                        'form': form,
                        'error': 'Please paste a job description.'
                    })
                try:
                    if not resume_text:
                        # Read the actual file from disk using its path
                        file_path = last.resume_file.path
                        print(f"Reading file from path: {file_path}")
                        with open(file_path, 'rb') as f:
                            import io
                            from .ai_analyzer import extract_text_from_pdf
                            file_obj = io.BytesIO(f.read())
                            resume_text = extract_text_from_pdf(file_obj)

                    print(f"Resume text length: {len(resume_text)}")
                    print(f"Preview: {resume_text[:200]}")

                    ai_result = analyze_resume(resume_text, job_description)
                    submission = ResumeSubmission(
                        resume_file=last.resume_file,
                        job_description=job_description,
                        feedback=ai_result,
                    )
                    submission.save()
                    return redirect('result', pk=submission.id)

                except Exception as e:
                    print(f"--- ERROR: {e} ---")
                    return render(request, 'screener/home.html', {
                        'form': form,
                        'error': str(e)
                    })
            else:
                return render(request, 'screener/home.html', {
                    'form': form,
                    'error': 'No saved resume found. Please upload a new one.'
                })

        # Normal new file upload flow
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = form.cleaned_data['resume_file']
            job_description = form.cleaned_data['job_description']
            resume_text = request.POST.get('resume_text', '').strip()

            try:
                if not resume_text:
                    import io
                    file_bytes = resume_file.read()
                    file_obj = io.BytesIO(file_bytes)
                    resume_text = extract_text_from_pdf(file_obj)
                    # Reset for saving
                    resume_file.seek(0)

                print(f"Resume text length: {len(resume_text)}")
                print(f"Preview: {resume_text[:200]}")

                if not resume_text:
                    return render(request, 'screener/home.html', {
                        'form': form,
                        'error': 'Could not read your PDF. Please paste your resume text in the box below instead.'
                    })

                ai_result = analyze_resume(resume_text, job_description)
                submission = ResumeSubmission(
                    resume_file=resume_file,
                    job_description=job_description,
                    feedback=ai_result,
                )
                submission.save()
                return redirect('result', pk=submission.id)

            except Exception as e:
                print(f"--- ERROR: {e} ---")
                return render(request, 'screener/home.html', {
                    'form': form,
                    'error': str(e)
                })
        else:
            print(f"--- Form invalid: {form.errors} ---")

    return render(request, 'screener/home.html', {'form': form})


def result(request, pk):
    submission = ResumeSubmission.objects.get(id=pk)
    return render(request, 'screener/result.html', {'submission': submission})