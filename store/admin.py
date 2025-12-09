from django.contrib import admin
from .models import Category, Customer, Product, Order, Profile
from django.contrib.auth.models import User

# Đăng ký các mô hình
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)

# Định nghĩa ProfileInLine để hiển thị thông tin Profile trong User Admin
class ProfileInLine(admin.StackedInline):
    model = Profile

# Định nghĩa UserAdmin để kết hợp thông tin User và Profile
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInLine]

# Hủy đăng ký mô hình User mặc định và đăng ký lại với UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Đăng ký Profile với admin, thêm trường old_cart vào list_display
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'old_cart']  # Hiển thị old_cart trong danh sách admin
    search_fields = ['user__username']  # Tìm kiếm theo tên người dùng
