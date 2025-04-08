from django.db import models
from django.contrib.postgres.fields import ArrayField  

class ResearchPaper(models.Model):
    title = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to="uploads/")
    extracted_text = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    insights = models.TextField(default="Insights not generated yet", blank=True)
    citation = models.TextField(default="", blank=True)
    named_entities = models.JSONField(default=list, blank=True, null=True)  # Store named entities as JSON
    embedding = models.JSONField(default=list, blank=True, null=True)       

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
