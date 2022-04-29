from email import message
import email
from math import prod
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.core.mail import send_mail,mail_admins, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

#uTo-code-import
from .forms import CreateUserForms, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
#uTo-code-import

def store(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
        
    products = Product.objects.all()
    comments = Comment.objects.all()
    context = {'products': products, 'cartItems':cartItems, 'post': comments}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items':items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def location(request):
    return render(request, 'store/location.html')

def collections(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
        
    products = Product.objects.all()
    context = {'products': products, 'cartItems':cartItems}
    return render(request, 'store/collections.html', context)

def contacts(request):
    if request.method == "POST":
        email = request.POST['email']
        message = request.POST['message']
        print(email + " " + message)
        # send_mail('Contact Form', 
        #           message,
        #           email, 
        #           ['avatar.gallery@mail.ru'], 
        #           fail_silently=False)
        mail_admins(email, 
                  message, 
                  fail_silently=False)
    return render(request, 'store/contacts.html')

def about(request):
    return render(request, 'store/about.html')

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('productId:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse('Payment complete', safe=False)


#uTo - code
@login_required(login_url='home')
def home(request):
    return render(request, 'store/home.html')

@login_required(login_url='profile')
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(request, f'{username}, Your profile is updated.')
            return redirect('/')
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'store/profile.html', context)

##@unauthenticated_user ne robit
def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'{username}, You are logged in.')
            return redirect("/")
        else:
            messages.info(request, 'Wrong password or username.')
            return redirect('login')
    return render(request, 'store/login_page.html')

##@unauthenticated_user ne robit
def register_user(request):
    form = CreateUserForms()

    if request.method == 'POST':
        form = CreateUserForms(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Account is created.')
            return redirect('login')
        else:
            context = {'form': form}
            messages.info(request, 'Invalid credentials.')
            return render(request, 'store/register_page.html', context)

    context = {'form': form}
    return render(request, 'store/register_page.html', context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.info(request, 'You logged out successfully')
    return redirect('login')
#/uTo - code
 

# class AddCommentView(CreateView):
#    model = Comment
#    template_name = 'add_comment.html'
#    fields = '__all__' 

# if request.method == "POST":
#        message_name = request.POST['message-name']
#        message_email = request.POST['message-email']
#        message = request.POST['message']
#        print(message_name+" "+"birnarse")
#        send_mail(
#            message_name, # subject
#            message, # message
#            message_email, # from email
#            ['avatar.gallery@mail.ru'], # to email
#        )
        
#        return render(request, 'store/contacts.html', {'message_name': message_name})
#    else:
#        return render(request, 'store/contacts.html', {})