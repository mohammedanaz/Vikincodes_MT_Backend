from django.contrib import admin
from .models import *

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ProductID', 'ProductCode', 'ProductName', 'CreatedDate', 'TotalStock')
    search_fields = ('id', 'ProductName', 'TotalStock')

@admin.register(Variant)
class VariantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')


@admin.register(SubVariant)
class SubVariantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'variant', 'name')
    search_fields = ('id', 'name')
