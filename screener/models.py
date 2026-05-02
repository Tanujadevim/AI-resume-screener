from django.db import models

class ResumeSubmission(models.Model):
    resume_file=models.FileField(upload_to="resumes/")
    job_description=models.TextField()
    submitted_at=models.DateTimeField(auto_now_add=True)
    match_score=models.FloatField(null=True,blank=True)
    feedback=models.TextField(null=True,blank=True)

    def __str__(self):
        return f"Submission #{self.id} - {self.submitted_at.strftime('%Y-%m-%d')}"