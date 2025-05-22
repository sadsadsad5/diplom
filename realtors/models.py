from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Realtor(models.Model):
  name = models.CharField("Имя",max_length=200)
  photo = models.ImageField("Фото",upload_to='photos/%Y/%m/%d/')
  description = models.TextField("Описание",blank=True)
  phone = models.CharField("Номер телефона",max_length=20)
  email = models.CharField(max_length=50)
  is_mvp = models.BooleanField("Лучший",default=False)
  hire_date = models.DateTimeField("Дата найма",default=datetime.now, blank=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "Риэлтор"
    verbose_name_plural = "Риэлторы"