from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


# Create your models here.
class Sheets(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    sheet_data = models.TextField(null = True, blank=True)

    def get_absolute_url(self):
        return reverse('modify', kwargs={'id': self.pk})

