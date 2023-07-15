from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Аккаунт')
    fullName = models.CharField(max_length=100, verbose_name='ФИО')
    name = models.CharField(max_length=60, verbose_name='Название')
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
    o_name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    plan_date = models.CharField(max_length=100, null=True, blank=True)
    change_date = models.CharField(max_length=100, null=True, blank=True)
    qu = models.CharField(max_length=100, null=True, blank=True)
    sqr = models.CharField(max_length=100, null=True, blank=True)
    transportinfo = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    floor = models.CharField(max_length=100, null=True, blank=True)
    c_name = models.CharField(max_length=100, null=True, blank=True)
    s_name = models.CharField(max_length=100, null=True, blank=True)    

class Route(models.Model):
    author = models.ForeignKey(Logist, on_delete=models.CASCADE, verbose_name="Логист")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name="Водитель")
    orders = models.ManyToManyField(Order)
    is_done = models.BooleanField(default=False)