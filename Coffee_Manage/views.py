from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Staff, Customer, Feedback, InventoryItem, Promotion
from .forms import MenuItemForm, StaffForm, CustomerForm, FeedbackForm, InventoryForm, PromotionForm

def dashboard(request):
    menu_form = MenuItemForm()

    # Xử lý form Menu POST
    if request.method == "POST" and 'menu_submit' in request.POST:
        menu_form = MenuItemForm(request.POST, request.FILES)
        if menu_form.is_valid():
            menu_form.save()
        else:
            print(menu_form.errors, flush=True)

    context = {
        'menu_items': MenuItem.objects.all(),  # menu list luôn được gửi xuống
        'menu_form': menu_form,
        'staff_list': Staff.objects.all(),
        'staff_form': StaffForm(),
        'customer_list': Customer.objects.all(),
        'customer_form': CustomerForm(),
    }
    return render(request, 'manager/dashboard.html', context)


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
