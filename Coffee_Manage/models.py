from django.db import models

class MenuItem(models.Model):
  name = models.CharField(max_length=100)
  image = models.ImageField(upload_to='menu_images/', blank=True)  # Lưu file vào media/menu_images
  category = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=6, decimal_places=2)
class Staff(models.Model):
  name = models.CharField(max_length=100)
  role = models.CharField(max_length= 50)
  email = models.EmailField()
  status = models.CharField(max_length=20, default='active')
  schedule = models.CharField(max_length=50, blank=True)
class Customer(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField()
  phone = models.CharField(max_length=20)
  totalOrders = models.IntegerField(default=0)
  totalSpent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  status = models.CharField(max_length=20, default='active')
class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    comment = models.TextField()
    foodRating = models.IntegerField(default=0)
    serviceRating = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='pending')
    response = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    supplier = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=20)
    minStock = models.IntegerField(default=0)
class Promotion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    discount = models.IntegerField()
    status = models.CharField(max_length=20, default='active')
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

