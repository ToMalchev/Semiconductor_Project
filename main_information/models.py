from django.db import models

# Create your models here.
class info_main(models.Model):
    image_1 = models.ImageField(upload_to = 'pic_folder/', default = 'static/information/img/lab.jpg')
    image_2 =models.ImageField(upload_to = 'pic_folder/', default = 'static/information/img/lab.jpg')
    block_1 = models.TextField(blank=True, default='')
    block_2 = models.TextField(blank=True, default='')