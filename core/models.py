from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Аккаунт')
    fullName = models.CharField(max_length=100, verbose_name='ФИО')
    name = models.CharField(max_length=60, verbose_name='Название')
    last_pos = models.CharField(max_length=100, null=True, blank=True)
    last_post_date_time = models.DateTimeField(null=True, blank=True)
    is_free = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return self.fullName
    
class Logist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Аккаунт')
    fullName = models.CharField(max_length=100, verbose_name='ФИО')
    phone_number = models.CharField(max_length=20, unique=True, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Логист'
        verbose_name_plural = 'Логисты'

    def __str__(self):
        return self.fullName
    

class Order(models.Model):
    o_name = models.CharField(max_length=256, null=True, blank=True, unique=True)
    plan_date = models.CharField(max_length=256)
    date_logist = models.CharField(max_length=256)
    qu = models.CharField(max_length=256)
    sqr = models.CharField(max_length=256)
    transportinfo = models.CharField(max_length=256)
    contact = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    floor = models.CharField(max_length=256)
    c_name = models.CharField(max_length=256)
    s_name = models.CharField(max_length=256)
    manager = models.CharField(max_length=256)
    calc_manager = models.CharField(max_length=256)
    delivery_sum = models.CharField(max_length=256)
    delivery_time = models.CharField(max_length=256)
    pos = models.CharField(max_length=60)
    response = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.o_name
    
class FileModel(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    file = models.FileField(upload_to="response/")

class Route(models.Model):
    author = models.ForeignKey(Logist, on_delete=models.CASCADE, verbose_name="Логист")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name="Водитель")
    route_link = models.URLField(max_length=1000)
    orders = models.ManyToManyField(Order)
    is_finish = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return self.author.fullName