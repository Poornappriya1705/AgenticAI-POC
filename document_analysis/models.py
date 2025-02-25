from django.db import models

def upload_to(instance, filename):
    return f"documents/{filename}"

class Document(models.Model):
    file = models.FileField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
