from django.db import models
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
    latitude = models.FloatField()
    longitude = models.FloatField()

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




