from .models import category

def all_category(req):
    all_category=category.objects.all()
    return {'all_category':all_category}