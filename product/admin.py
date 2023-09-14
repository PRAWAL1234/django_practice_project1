from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Products)
class productAdmin(admin.ModelAdmin):
    list_display=('id','product_name','price','stock','category','created_date')
    prepopulated_fields={'slug':('product_name',)}

@admin.register(variation)
class variationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value')