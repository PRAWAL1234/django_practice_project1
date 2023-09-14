from .models import CartItem

def cart_item_count(req):
    user=req.user
    if user.is_authenticated:
        total_item=CartItem.objects.filter(user=user).count()
    else:
        total_item=0
    return {'cart_total_item':total_item}