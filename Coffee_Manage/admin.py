from django.contrib import admin
from .models import MenuItem, Staff, Customer, Feedback, InventoryItem, Promotion

# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(Feedback)
admin.site.register(InventoryItem)
admin.site.register(Promotion)