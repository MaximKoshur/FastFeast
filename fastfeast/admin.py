from django.contrib import admin
from .models import Dishes, User, CategoryDishes, CategoryInstitution, Basket, BasketProduct, Institution

admin.site.register(Dishes)
admin.site.register(User)
admin.site.register(CategoryInstitution)
admin.site.register(CategoryDishes)
admin.site.register(Basket)
admin.site.register(BasketProduct)
admin.site.register(Institution)



