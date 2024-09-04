from django.db import models


class upload(models.Model):
    title = models.CharField(max_length=50)
    upload = models.FileField(upload_to="media")

    def __str__(self):
        return f"{self.title}"