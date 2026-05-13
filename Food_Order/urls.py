from django.contrib import admin
from django.urls import path
from accounts.views import *
from core.views import *
from products.views import *
from orders.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('menu/', menu, name='menu'),
    path('product_list/<int:id>', product_list, name='product_list'),
    path('popular_dishes/', popular_dishes, name='popular_dishes'),
    path('restaurant/', restaurant, name='restaurant'),
    path('restaurant/view_menu/<int:id>', view_menu, name='view_menu'),
    path('category/', category, name='Category'),
    path('cart/', cart_page, name='cart_page'),
    path('increase_quantity/<int:id>', increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:id>', decrease_quantity, name='decrease_quantity'),
    path('remove_item/<int:id>', remove_item, name='remove_item'),
    path('add_item_cart/<int:id>',add_item_cart, name='add_item_cart'),
    path('checkout/',checkout, name='checkout'),
    path('place_order/',place_order, name='place_order'),
    path('verify_payment/', verify_payment, name='verify_payment'),
    path('order_success/<int:id>/',order_success, name='order_success'),
    path('my_orders/',my_orders, name='my_orders'),
    path('track_your_order/<int:id>',order_tracking, name='order_tracking'),
    path('change_address/',change_address,name='change_address'),
    path('make_default_address/<int:id>',make_default_address,name='make_default_address'),
    path('add_new_address/',add_new_address,name='add_new_address'),
    path('update_address/<int:id>',update_address,name='update_address'),
    path('cancel_order/<int:id>/', cancel_order, name='cancel_order'),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# ADD THIS 👇 (SERVE MEDIA FILES)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)