from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return self.password and make_password(raw_password, self.password)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # if product is degital we can't ship it
    #digital = models.BooleanField(default=False, null=True, blank=True)
    images = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    #for image error if it doesn't exist
    @property
    def imageURL(self):
        try:
            url = self.images.url
        except:
            url = ''
        return url

 
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # if complete is false we still can add more to cart
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True,)

    def __str__(self):
        return str(self.id)
    
    #total cart value
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    #total cart items
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
