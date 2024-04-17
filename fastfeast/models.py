from django.db import models
from django.contrib.auth.models import AbstractUser
from .yamaps import geocoder


class Dishes(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey("CategoryDishes", on_delete=models.CASCADE, related_name='dishes')
    institution = models.ForeignKey("Institution", on_delete=models.CASCADE, related_name='dishes')

    class Meta:
        verbose_name_plural = 'Блюда'
        verbose_name = 'Блюдо'
        ordering = ['name']

    def __str__(self):
        return self.name


class CategoryDishes(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Категории блюд'
        verbose_name = 'Категория блюд'
        ordering = ['name']

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey("CategoryInstitution", on_delete=models.CASCADE, related_name='institutions')
    address = models.TextField(max_length=50)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if self.address:
            lat, lon = geocoder(self.address)
            self.latitude = lat
            self.longitude = lon

        super(Institution, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Заведения'
        verbose_name = 'Заведение'
        ordering = ['name']

    def __str__(self):
        return self.name


class CategoryInstitution(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Категории заведений'
        verbose_name = 'Категория заведений'
        ordering = ['name']

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    address = models.TextField(max_length=50)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def save(self, *args, **kwargs):
        if self.address:
            lat, lon = geocoder(self.address)
            self.latitude = lat
            self.longitude = lon
        super(CustomUser, self).save(*args, **kwargs)


class Order(models.Model):
    class Status(models.TextChoices):
        INPROGRESS = 'INPROGRESS', 'Собирается пользователем'
        PREPARE = 'PREPARE', 'Готовится'
        ONTHEWAY = 'ONTHEWAY', 'В пути'
        DELIVERED = 'DELIVERED', 'Доставлен'

    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INPROGRESS)

    def total_price(self):
        total_price = 0
        for entry in self.order_entries.all():
            total_price += entry.dish.price * entry.count
        return total_price

    def total_count(self):
        total_count = 0
        for entry in self.order_entries.all():
            total_count += entry.count
        return total_count


class OrderEntry(models.Model):
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE, related_name='+')
    count = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_entries')


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shopping_cart = models.OneToOneField(Order, on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='+')

    def __str__(self):
        return self.user.username

