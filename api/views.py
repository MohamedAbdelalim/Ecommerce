from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from api.forms import CustomerForm
from .models import Customer, Product, Order, OrderItem
import json


def registerPage(request):
    if request.user.is_authenticated:
        
        return redirect('store')
    
    else:

        form = CustomerForm()
        if request.method == 'POST':

            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')

        context = {'form': form}
        return render(request, 'api/register.html', context)
    
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')

    else:
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username ,password=password)
            if user is not None:          
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request,'api/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def store(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'api/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        #create if not exisr
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items': items, 'order':order}
    return render(request, 'api/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # create if not exist
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'api/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

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
