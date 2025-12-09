from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem, Staff, Customer, Feedback, InventoryItem, Promotion
from .forms import MenuItemForm, StaffForm, CustomerForm, FeedbackForm, InventoryForm, PromotionForm
from django.http import JsonResponse
from django.db.models import Sum, Count, F
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from django.http import JsonResponse
from .models import MenuItem, Staff, Order, OrderItem
from .forms import MenuItemForm, StaffForm
import json

def dashboard(request):
    context = {
        "menu_items": MenuItem.objects.all(),
        "staff_list": Staff.objects.all(),
        "menu_form": MenuItemForm(),
        "staff_form": StaffForm(),
        "feedback_list": Feedback.objects.all(),
        "active_tab": "menu"
    }
    return render(request, "manager/dashboard.html", context)
def menu_add(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)  # nhớ request.FILES
        if form.is_valid():
            menu = form.save()
            image_url = menu.image.url if menu.image else ""
            return JsonResponse({
                "success": True,
                "menu": {
                    "id": menu.id,
                    "name": menu.name,
                    "category": menu.category,
                    "price": str(menu.price),
                    "image_url": image_url
                }
            })
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "error": "Invalid request"})
def menu_delete(request):
    if request.method == "POST":
        menu_id = request.POST.get("menu_id")
        if menu_id and menu_id.isdigit():
            MenuItem.objects.filter(id=int(menu_id)).delete()
            return JsonResponse({"success": True, "qty": MenuItem.objects.count()})
        return JsonResponse({"success": False, "error": "Invalid menu ID"})
    return JsonResponse({"success": False, "error": "Invalid request"})
def staff_add(request):
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            staff = form.save()
            # Trả về JSON thông tin staff mới để append vào DOM
            return JsonResponse({
                "success": True,
                "staff": {
                    "id": staff.id,
                    "name": staff.name,
                    "role": staff.role,
                    "email": staff.email,
                }
            })
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse({"success": False, "error": "Invalid request"})

def staff_delete(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        if staff_id and staff_id.isdigit():
            Staff.objects.filter(id=int(staff_id)).delete()
            return JsonResponse({"success": True, "qty": Staff.objects.count()})
        return JsonResponse({"success": False, "error": "Invalid staff ID"})
    return JsonResponse({"success": False, "error": "Invalid request"})
def feedback_reply(request):
    if request.method == "POST":
        feedback_id = request.POST.get("feedback_id")
        response = request.POST.get("response", "").strip()
        if feedback_id and feedback_id.isdigit() and response:
            feedback = Feedback.objects.filter(id=int(feedback_id)).first()
            if feedback:
                feedback.response = response
                feedback.status = "responded"
                feedback.save()
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "error": "Feedback not found"})
        return JsonResponse({"success": False, "error": "Invalid input"})
    return JsonResponse({"success": False, "error": "Invalid request"})
def feedback_delete(request):
    if request.method == "POST":
        feedback_id = request.POST.get("feedback_id")
        if feedback_id and feedback_id.isdigit():
            Feedback.objects.filter(id=int(feedback_id)).delete()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "Invalid feedback ID"})
    return JsonResponse({"success": False, "error": "Invalid request"})
def report_revenue(request):
    if request.method != "GET":
        return JsonResponse({"success": False, "error": "Invalid request"})

    try:
        # Lấy top 5 món bán chạy
        top_items = (
            OrderItem.objects
            .values("menu_item__name")
            .annotate(total_sold=Coalesce(Sum("quantity"), 0))
            .order_by("-total_sold")[:5]
        )

        # Chuẩn bị dữ liệu cho Chart.js
        labels = [item["menu_item__name"] for item in top_items]
        sold = [item["total_sold"] for item in top_items]

        # Thống kê doanh thu
        today = timezone.now().date()
        month_start = today.replace(day=1)

        revenue_today = (
            Order.objects
            .filter(created_at__date=today)
            .aggregate(total=Coalesce(Sum("total_price"), 0))
            .get("total")
        )
        revenue_month = (
            Order.objects
            .filter(created_at__date__gte=month_start)
            .aggregate(total=Coalesce(Sum("total_price"), 0))
            .get("total")
        )
        avg_order = (
            Order.objects
            .aggregate(avg=Coalesce(Sum("total_price") / Count("id"), 0))
            .get("avg")
        )
        context = {
            "top_items": top_items,

            # JSON Chart.js
            "labels_json": json.dumps(labels),
            "sold_json": json.dumps(sold),

            # Revenue statistics
            "revenue_today": revenue_today,
            "revenue_month": revenue_month,
            "avg_order": avg_order,
            "active_tab": "revenue_report"
        }
        return render(request, "manager/revenue_report.html", context)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
