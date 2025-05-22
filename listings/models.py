from django.db import models
from datetime import datetime
from realtors.models import Realtor
from django.contrib.auth.models import User


class Listing(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING, verbose_name="Риэлтор", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь", null=True, blank=True)
    title = models.CharField("Название", max_length=200)
    address = models.CharField("Адрес", max_length=200)
    city = models.CharField("Город", max_length=100)
    state = models.CharField("Область", max_length=100)
    zipcode = models.IntegerField("Год постройки")
    description = models.TextField("Описание", blank=True)
    price = models.IntegerField("Цена")
    bedrooms = models.IntegerField("Количество комнат")
    bathrooms = models.DecimalField("Ванные комнаты", max_digits=2, decimal_places=1)
    garage = models.IntegerField("Гараж", default=0)
    sqft = models.IntegerField("Площадь")
    lot_size = models.DecimalField("Площадь участка", max_digits=5, decimal_places=1)
    photo_main = models.ImageField("Главное фото", upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField("Фото 1", upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField("Фото 2", upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField("Фото 3", upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField("Фото 4", upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField("Фото 5", upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField("Фото 6", upload_to='photos/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField("Опубликовать", default=False)
    list_date = models.DateTimeField("Дата договора", default=datetime.now, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
