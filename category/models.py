from django.db import models

# Create your models here.
class category(models.Model):
    category_name=models.CharField(max_length=200,unique=True)
    slug=models.CharField(max_length=200,unique=True)
    description=models.TextField(blank=True)
    
    def __str__(self):
        return self.category_name