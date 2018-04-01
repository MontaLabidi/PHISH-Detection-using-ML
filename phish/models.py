from django.db import models

# Create your models here.

class Tested_URLs(models.Model):
    url=models.URLField(max_length=1000)
    phishing=models.IntegerField()
    #submissions=models.IntegerField(max_length=10000)