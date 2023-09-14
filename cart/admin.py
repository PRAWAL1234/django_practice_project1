from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(cart)

class cartAdmin(admin.ModelAdmin):
    list_display=('user_id','created_date')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=('product','quantity','user','is_active','id')
