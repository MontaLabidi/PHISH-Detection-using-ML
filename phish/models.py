from django.db import models


class REVIEWS(models.Model):
    ip = models.GenericIPAddressField(null=True)
    msg = models.TextField(null=True)
    rate = models.CharField(max_length=5)

    def __str__(self):
        return self.msg


class URL(models.Model):
    name = models.URLField()
    phish = models.BooleanField(default=True)
    occ = models.IntegerField(null=True)

    def __str__(self):
        return self.name
