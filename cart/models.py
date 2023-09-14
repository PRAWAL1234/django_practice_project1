from django.db import models
from product.models import *
from django.contrib.auth.models import User

class cart(models.Model):
    user_id=models.CharField(max_length=255)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id

class CartItem(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    variation=models.ManyToManyField(variation)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    # def __str__(self):
    #     return self.product.product_name
    
    # def __str__(self):
    #     return self.product.price*self.quantity