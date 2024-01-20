from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from pathlib import Path

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = "Аккаунт")
    fullName = models.CharField(max_length = 100, verbose_name = "ФИО")
    name = models.CharField(max_length = 60, verbose_name = "Название")
    last_pos = models.CharField(max_length = 100, null = True, blank = True)
    last_post_date_time = models.DateTimeField(null = True, blank = True)
    is_free = models.BooleanField(default = True)
    phone_number = models.CharField(max_length = 20, unique = True, verbose_name = "Телефон")

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"

    def __str__(self):
        return self.fullName
    
class Logist(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = "Аккаунт")
    fullName = models.CharField(max_length = 100, verbose_name = "ФИО")
    phone_number = models.CharField(max_length = 20, unique = True, verbose_name = "Телефон")

    class Meta:
        verbose_name = "Логист"
        verbose_name_plural = "Логисты"

    def __str__(self):
        return self.fullName
    

class Order(models.Model):
    o_name = models.CharField(max_length = 256, null = True, blank = True, unique = True, verbose_name = "#")
    plan_date = models.CharField(max_length = 256, verbose_name = "Дата")
    date_logist = models.CharField(max_length = 256, verbose_name = "Дата логиста")
    qu = models.CharField(max_length = 256, verbose_name = "Количество")
    sqr = models.CharField(max_length = 256, verbose_name = "Площадь")
    transportinfo = models.CharField(max_length = 256, verbose_name = "Комментарий")
    contact = models.CharField(max_length = 256, verbose_name = "Контакт")
    address = models.CharField(max_length = 256, verbose_name = "Адрес")
    phone = models.CharField(max_length = 256, verbose_name = "Телефон")
    floor = models.CharField(max_length = 256, verbose_name = "Этаж")
    c_name = models.CharField(max_length = 256, verbose_name = "Клиент")
    s_name = models.CharField(max_length = 256, verbose_name = "Статус")
    manager = models.CharField(max_length = 256, verbose_name = "Менеджер")
    calc_manager = models.CharField(max_length = 256, verbose_name = "Расчетчик")
    delivery_sum = models.CharField(max_length = 256, verbose_name = "Сумма доставки")
    delivery_time = models.CharField(max_length = 256, verbose_name = "Время")
    pos = models.CharField(max_length = 60, verbose_name = "Локация")
    call_status = models.CharField(max_length = 60, default = "no call", verbose_name = "Статус звонка")
    call_audio = models.FileField(null = True, blank = True, upload_to="audio", verbose_name = "Результат созвона в аудио")
    call_text = models.TextField(default = "no call", verbose_name = "Результат созвона в текстовом виде")
    response = models.BooleanField(default = False)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.o_name
    
class FileModel(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    file = models.FileField(upload_to = "response/")

class Route(models.Model):
    author = models.ForeignKey(Logist, on_delete = models.CASCADE, verbose_name = "Логист")
    driver = models.ForeignKey(Driver, on_delete = models.CASCADE, null = True, blank = True, verbose_name = "Водитель")
    route_link = models.URLField(max_length = 1000)
    orders = models.ManyToManyField(Order)
    is_call = models.BooleanField(default = True)
    is_finish = models.BooleanField(default = False)

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

    def __str__(self):
        return self.author.fullName