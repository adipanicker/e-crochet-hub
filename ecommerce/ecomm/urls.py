"""
URL configuration for ecomm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views   # <-- replace app_name with your actual app folder

urlpatterns = [
    path('admin/', admin.site.urls),

    # ---------- Home & Category ----------
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    # path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # ---------- Auth ----------
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

# Category standalone pages
    path('accessories/', views.accessories, name='accessories'),
    path('clothings/', views.clothings, name='clothings'),
    path('bags/', views.bags, name='bags'),
    path('decor_items/', views.decor_items, name='decor_items'),
    # ---------- Feedback ----------
    # path('feedback/', views.feedback_view, name='feedback'),
    path('feedback/', views.feedback_page, name='feedback'),
    path("contact/", views.contact, name="contact"),



    # Cart system
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('increase-qty/<int:product_id>/', views.increase_qty, name='increase_qty'),
    path('decrease-qty/<int:product_id>/', views.decrease_qty, name='decrease_qty'),
    path('remove-item/<int:product_id>/', views.remove_item, name='remove_item'),


    # Checkout & Orders  (FIXED)
    path("checkout/", views.checkout, name="checkout"),
    path("confirm-order/", views.confirm_order, name="confirm_order"),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
    path("my_orders/", views.my_orders, name="my_orders"),

    # path("payment/", views.payment_test, name="payment_test"),
    path("payment/<int:order_id>/", views.payment_test, name="payment_test"),

    path("pay/<int:order_id>/", views.payment_test, name="payment_test"),
    path("order/success/<int:order_id>/", views.order_success, name="order_success"),

    #whishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    #invoice_download
    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),

]



# Serve images during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
