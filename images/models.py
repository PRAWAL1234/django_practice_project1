from django.db import models

# Create your models here.
class image(models.Model):
    image=models.ImageField(upload_to='background')
    created_date=models.DateField(auto_now_add=True)

    