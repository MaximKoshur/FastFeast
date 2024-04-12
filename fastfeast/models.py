from django.db import models
from django.contrib.auth.models import AbstractUser


class Dishes(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey("CategoryDishes", on_delete=models.CASCADE)

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
    category = models.ForeignKey("CategoryInstitution", on_delete=models.CASCADE)

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


class Basket(models.Model):
    class Status(models.TextChoices):
        INITIAL = 'INITIAL', 'Initial'
        COMPLETED = 'COMPLETED', 'Completed'
        DELIVERED = 'DELIVERED', 'Delivered'

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='baskets')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIAL)

    class Meta:
        verbose_name_plural = 'Корзины покупок'
        verbose_name = 'Корзина покупок'

    # def __str__(self):
    #     return self.name

    def total_price(self):
        total_price = 0
        for entry in self.basket_product.all():
            total_price += entry.dish.price * entry.count
        return total_price

    def total_count(self):
        total_count = 0
        for entry in self.basket_product.all():
            total_count += entry.count
        return total_count


class BasketProduct(models.Model):
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE, related_name='+')
    count = models.IntegerField(default=0)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='basket_product')

    class Meta:
        verbose_name_plural = 'Блюда в корзинах'
        verbose_name = 'Блюдо в корзине'

    # def __str__(self):
    #     return self.name


class User(AbstractUser):
    basket = models.OneToOneField(Basket, on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='+')

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
