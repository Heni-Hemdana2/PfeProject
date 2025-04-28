from django.db                      import models

class data(models.Model):
    pseudo   = models.CharField(max_length=30)
    password    = models.CharField(max_length=128)