from django.shortcuts import render,HttpResponse,redirect
from product.models import *
from images.models import *
from django.core.paginator import Paginator
from django.contrib import auth
from cart.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from admin.form import sign
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

def login(req):
   if req.method =='POST':
      username=req.POST['username']
      password=req.POST['password']
      user=auth.authenticate(username=username,password=password)

      if user is not None:
         auth.login(req,user)
         messages.add_message(req,messages.SUCCESS,'Login Successfull')
         return redirect('/')
         
      else:
         messages.add_message(req,messages.ERROR,'User does not exists')
         return render(req,'accounts/login.html') 
   return render(req,'accounts/login.html')

def logout(req):
    auth.logout(req)
    return redirect('/')

def signup(req):
   
    form=sign()
    
    if req.method == 'POST':
       form=sign(req.POST)

       if form.is_valid():
          print('d1')
          first_name=req.POST['first_name']
          last_name=req.POST['last_name']
          email=req.POST['email']
          username=req.POST['username']
          password=req.POST['password']
          user=User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password,is_active=False)
          user.save()
          form=sign()
          domain_name=get_current_site(req)
          mail_subject="PLease Activate Account"
          user_id=urlsafe_base64_encode(force_bytes(user.pk))
          token=default_token_generator.make_token(user)
          message=f'http://{domain_name}/accounts/activation/{user_id}/{token}'
          to_email=email

          print('d8')
          send_mail=EmailMessage(mail_subject,message,to=[to_email])
          send_mail.send()
          print('d9')
          
          messages.add_message(req,messages.SUCCESS,'SIGNUP SUCCESSFULLY')  
       else:
          print('d10')
          messages.add_message(req,messages.ERROR,'Invalid Information',extra_tags='danger')
    context={
       'form':form
    }

    return render(req,'accounts/sign.html',context)

def active(req,id,token):
    try:
       pk=urlsafe_base64_decode(id)
       user=User.objects.get(pk=pk)
       if default_token_generator.check_token(user,token):
          user.is_active=True
          user.save()
          messages.add_message(req,messages.SUCCESS,'Verification Successfully')
    except:
       messages.add_message(req,messages.ERROR,'Invalid credentails')
    return redirect('/sign')

def forgot(req):
   if req.method =='POST':
      email=req.POST['email']
      user=User.objects.get(email=email)

      if user:
         domain_name=get_current_site(req)
         mail='Reset Password'
         user_id=urlsafe_base64_encode(force_bytes(user.pk))
         token=default_token_generator.make_token(user)
         message=f'http://{domain_name}/reset-password/{user_id}/{token}'
         to_email=email
         send_mail=EmailMessage(mail,message,to=[to_email])
         send_mail.send()
         messages.add_message(req,messages.SUCCESS,'Reset Link Send To Your Email')
      else:
        messages.add_message(req,messages.ERROR,'No Email Exists')
   return render(req,'accounts/forgot.html')

def resetpassword(req,id,token):
   try:
      id=urlsafe_base64_decode(id)
      user=User.objects.get(id=id)

      if default_token_generator.check_token(user,token):
         req.session['uid']=id
         return render(req,'accounts/resetpassword.html')
   except:
       return redirect('/sign')

def home(req):
    products=Products.objects.all()
    images=image.objects.all()
    context={
        'product':products,
        'image':images
    }
    return render(req,'home.html',context)

def store(req):
    categorys=category.objects.all()
    product=Products.objects.all()
    paginator=Paginator(product,8)

    try:
        page=req.GET['page']
    except:
        page=1

    Product=paginator.get_page(page)

    context={
        'category':categorys,
        'product':Product
    }
    return render(req,'store/store.html',context)

def details(req,id):
    Product=Products.objects.get(id=id)
    color=variation.objects.filter(product=Product,variation_category='color')
    size=variation.objects.filter(product=Product,variation_category='size')
    context={
        'product':Product,
        'color':color,
        'size':size
    }
    return render(req,'store/details.html',context)

def Category(req,id):
    Product=Products.objects.filter(category__category_name=id)
    categorys=category.objects.all()
    context={
        'product':Product,
        'category':categorys
    }
    return render(req,'store/store.html',context)

@login_required(login_url='/')
def addcart(request,id):
    product=Products.objects.get(id=id)
    user=request.user


    if request.method =="POST":
        color=request.POST['color']
        size=request.POST['size']
        print(size,color)
        size_variant=variation.objects.get(variation_value=size,product=product)
        color_variant=variation.objects.get(variation_value=color,product=product)
    
        current_variant= [color_variant,size_variant]

        is_product_exists= CartItem.objects.filter(product= product,user=user).exists()

        if is_product_exists:
          
          each_product_variants= []
          products=  CartItem.objects.filter(product= product,user=user)

          for product in products:
            each_product_variants.append(list(product.variation.all()))

          if  current_variant in each_product_variants:
            product_index=  each_product_variants.index(current_variant)
            product= products[product_index]
            product.quantity += 1
            product.save()


          else:
            product=Products.objects.get(id=id)
            cart_item=CartItem.objects.create(product=product,user=user,quantity=1)
            cart_item.variation.add(size_variant) 
            cart_item.variation.add(color_variant)  

            
        
        else:
          cart_item=CartItem.objects.create(product=product,user=user,quantity=1)
          cart_item.variation.add(size_variant) 
          cart_item.variation.add(color_variant) 
       
    return redirect('/cart')    


@login_required(login_url='/')
def Cart(req):
   user=req.user
   all_cart_item=CartItem.objects.filter(user=user)
   t=0

   for cart_item in all_cart_item:
      t+=cart_item.product.price * cart_item.quantity
    
   
   context={
       'all_cart_item':all_cart_item,
       'total':t,
       'tax':round(t*0.18,2),
       'grand_total':round(t+t*0.18+50,2)
    
   }
   return render(req,'store/cart.html',context)

@login_required(login_url='/')
def removecart(req,id):
   user=req.user
   print('d1')
   cart_item=CartItem.objects.get(id=id,user=user)
   print('d2')
   
   if cart_item.quantity>1:
      print('f1')
      cart_item.quantity-=1
      cart_item.save()
   else:
      print('f2')
      cart_item.delete()    

   return redirect('/cart')


def remove_cart_item(req,id):
   user=req.user
   ct=CartItem.objects.get(product=id,user=user)
   ct.delete()
   return redirect('/cart')