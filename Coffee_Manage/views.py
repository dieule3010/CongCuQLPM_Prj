from django.shortcuts import render
from . models import MenuItem, Staff, Customer, Feedback, InventoryItem, Promotion

def dashboard(request):
    context = {
        'menu_items': MenuItem.objects.all(),
        'staff': Staff.objects.all(),
        'customers': Customer.objects.all(),
        'feedback': Feedback.objects.all(),
        'inventory': InventoryItem.objects.all(),
        'promotions': Promotion.objects.all(),
    }
    return render(request, 'manager/dashboard.html', context)

def menu_management(request):
    items = MenuItem.objects.all()
    return render(request, 'manager/menu.html', {'menu_items': items})

def staff_management(request):
    staff = Staff.objects.all()
    return render(request, 'manager/staff.html', {'staff': staff})

def customer_management(request):
    customers = Customer.objects.all()
    return render(request, 'manager/customers.html', {'customers': customers})

def feedback_management(request):
    feedback = Feedback.objects.all()
    return render(request, 'manager/feedback.html', {'feedback': feedback})

def inventory_management(request):
    inventory = InventoryItem.objects.all()
    return render(request, 'manager/inventory.html', {'inventory': inventory})

def promotions_management(request):
    promotions = Promotion.objects.all()
    return render(request, 'manager/promotions.html', {'promotions': promotions})
