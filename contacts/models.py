from django.db import models
from datetime import datetime

class Contact(models.Model):
  listing = models.CharField("Объявление",max_length=200)
  listing_id = models.IntegerField("Номер объявления")
  name = models.CharField("Имя",max_length=200)
  email = models.CharField(max_length=100)
  phone = models.CharField("Номер телефона",max_length=100)
  message = models.TextField("Сообщение",blank=True)
  contact_date = models.DateTimeField("Дата обращения",default=datetime.now, blank=True)
  user_id = models.IntegerField("ID пользователя",blank=True)
  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "Контакт"
    verbose_name_plural = "Контакты"