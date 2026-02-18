from django.contrib import admin
from .models import (
    Feedback,
    Category,
    Product,
    Contact,
    Order,
    OrderItem,
    # Wishlist
)

# ===================== FEEDBACK ADMIN =====================
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('rating', 'created_at')

admin.site.register(Feedback, FeedbackAdmin)


# ===================== CATEGORY & PRODUCT =====================
admin.site.register(Category)
admin.site.register(Product)


# ===================== CONTACT =====================
admin.site.register(Contact)


# ===================== ORDER =====================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'full_name',
        'phone',
        'order_status', 
        'total_amount',
        'payment_method',
        'payment_status',
        'created_at'
    )
    search_fields = ('id', 'full_name', 'phone', 'user__username')
    list_filter = ('payment_method', 'payment_status', 'created_at')
    list_editable = ("order_status",)#admin can change status
    inlines = [OrderItemInline]


# ===================== ORDER ITEMS =====================
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'qty', 'price')
    search_fields = ('order__id', 'product__name')

# ===================== wishlist =====================
# @admin.register(Wishlist)
# class WishlistAdmin(admin.ModelAdmin):
#     list_display = ('user', 'product', 'created_at')

