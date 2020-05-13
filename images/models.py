from django.db import models


class Images(models.Model):
    name = models.TextField(max_length=50)
    image = models.ImageField(upload_to='images/')

