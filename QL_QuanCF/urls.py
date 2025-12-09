from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # App Store (trang chủ Ecommerce)
    path('', include('store.urls')),

    # App Coffee (nếu bạn muốn)
    path('coffee/', include('Coffee_Manage.urls')),

    # App Payment (đúng app)
    path('payment/', include('payment.urls')),
    path('cart/', include('cart.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
