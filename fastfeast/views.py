from django.shortcuts import render
from .models import Dishes, User, CategoryDishes, CategoryInstitution, Basket, BasketProduct, Institution


def main(request):
    context = {"institutions": Institution.objects.all()}
    return render(request, 'fastfeast/main.html', context)
