from django.db import models

class contactDetail(models.Model):
    name = models.CharField(max_length=30)
    tel = models.IntegerField()
    addr = models.CharField(max_length=40)
    def __str__(self):
        return '%s' % self.name