from django.db import models

# Create your models here.
class Article(models.Model):
    judul = models.CharField(max_length=255)
    isi = models.TextField()