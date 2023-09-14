from django.contrib import admin
from .models import category
# Register your models here.
@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
    list_display=('slug','category_name')
    prepopulated_fields={'slug':('category_name',)}