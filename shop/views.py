from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
from .form import CustomUserForm 
from django.contrib.auth import authenticate,login,logout
import json
from django.http import JsonResponse


def home(request):
    products = Product.objects.filter(trending=1)
    return render(request,'shop/index.html',{"products":products})

def fav_view_page(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
  
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/fav_view_page")
  
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")
    
def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return  render(request,"shop/cart.html",{"cart":cart})
    else:
        return redirect('/')
    
def remove_cart(request,cid):
    cart_item = get_object_or_404(Cart, id=cid, user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect("/cart")
    
def add_to_cart(request):
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'Invalid access'}, status=400)

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Login required'}, status=401)

    data = json.loads(request.body)
    product_id = data.get('pid')
    product_qty = data.get('product_qty')

    if not product_id or not product_qty:
        return JsonResponse({'status': 'Invalid data'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'Product not found'}, status=404)

    if product.quantity < product_qty:
        return JsonResponse({'status': 'Product out of stock'}, status=400)

    if Cart.objects.filter(user=request.user, product_id=product_id).exists():
        return JsonResponse({'status': 'Product already in cart'}, status=200)

    Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
    return JsonResponse({'status': 'Product added to cart'}, status=200)

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
 
        
def login_page(request):
    if request.method=="POST":
        name = request.POST.get("username")
        pwd = request.POST.get("password")
        user = authenticate(username=name,password=pwd)
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in Successfully")
            return redirect("/")
        else:
            messages.error(request,"Invalid User Name or Password")
            return redirect("/login")
    return render(request,'shop/login.html')
    
def logout_page(request):
    if User.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully")
    return redirect("/")
    
    
def register(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Success You can login now ')
            return redirect('/login')
    return render(request,'shop/register.html',{"form":form})

def collections (request):
    catagory = Catageory.objects.filter(status=0)
    return  render(request,'shop/collections.html',{"catagory":catagory})
    
def collectionview(request,name):
    if(Catageory.objects.filter(name=name,status=0)):
        products = Product.objects.filter(catageory__name=name)
        return render(request,"shop/products/index.html",{"products":products,"category_name":name})
    else:
        messages.warning(request,"No such item found")
        return redirect('collections')
    
def product_details(request,cname,pname):
    if(Catageory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname)):
            products = Product.objects.filter(name=pname,status=0).first()
            return render(request,'shop/products/product_details.html',{"products":products})
        else:
            messages.error(request,"No such Product found")
            return redirect('collections')
    else:
        messages.error(request,"No Such Catageory Found")
        return redirect('collections')
        