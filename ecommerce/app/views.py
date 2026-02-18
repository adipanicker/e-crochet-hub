from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Category
from .models import Order, OrderItem
from .models import Feedback, Category, Product
from .models import Wishlist, Product


# ========================== HOME =============================

def home(request):
    categories = Category.objects.all()
    return render(request, "home.html", {"categories": categories})


# ========================== AUTH =============================

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("home")


# ======================== FEEDBACK ============================

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Feedback

def feedback_page(request):
    feedback_list = Feedback.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        # User can submit feedback
        if request.method == "POST":
            Feedback.objects.create(
                name=request.user.first_name or request.user.username,
                email=request.user.email,
                message=request.POST.get("message"),
                rating=request.POST.get("rating"),
            )
            messages.success(request, "Thank you for your feedback!")
            return redirect("feedback")
    return render(request, "feedback.html", {"feedback_list": feedback_list})

# ======================== CATEGORY PAGES =======================

def accessories(request):
    cat = Category.objects.filter(name__iexact="Accessories").first()
    products = Product.objects.filter(category=cat)
    return render(request, "accessories.html", {"products": products})


def clothings(request):
    cat = Category.objects.filter(name__iexact="Clothings").first()
    products = Product.objects.filter(category=cat)
    return render(request, "clothings.html", {"products": products})


def bags(request):
    cat = Category.objects.filter(name__iexact="Bags").first()
    products = Product.objects.filter(category=cat)
    return render(request, "bags.html", {"products": products})


def decor_items(request):
    cat = Category.objects.filter(name__iexact="Decor Items").first()
    products = Product.objects.filter(category=cat)
    return render(request, "decor_items.html", {"products": products})


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


# ========================== CART SYSTEM ========================

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.qty += 1
        cart_item.save()
    return redirect("cart")


@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in items)
    return render(request, "cart.html", {"items": items, "total": total})

@login_required
def increase_qty(request, product_id):
    item = Cart.objects.get(product_id=product_id, user=request.user)
    item.qty += 1
    item.save()
    return redirect("cart")



@login_required
def decrease_qty(request, product_id):
    item = Cart.objects.get(product_id=product_id, user=request.user)
    if item.qty > 1:
        item.qty -= 1
        item.save()
    else:
        item.delete()
    return redirect("cart")


@login_required
def remove_item(request, product_id):
    Cart.objects.get(product_id=product_id, user=request.user).delete()
    return redirect("cart")



@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in items)
    return render(request, "cart.html", {"items": items, "total": total})


@login_required
def checkout(request):
    return render(request, "checkout.html")

def category_products(request, category_id):
    category = Category.objects.get(id=category_id)

    if category.name.lower() == "handcrafted":
        return redirect("handcrafted")

    elif category.name.lower() == "homecrafted":
        return redirect("homecrafted")

    # optional fallback
    return redirect("home")


@login_required
def update_cart(request, item_id, action):
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        if action == "increase":
            cart[str(item_id)] += 1
        elif action == "decrease":
            cart[str(item_id)] -= 1
            if cart[str(item_id)] <= 0:
                del cart[str(item_id)]
        elif action == "remove":
            del cart[str(item_id)]

    request.session['cart'] = cart
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})

    item_id = str(item_id)

    if item_id in cart:
        del cart[item_id]

    request.session['cart'] = cart
    return redirect('cart')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("/contact")

    return render(request, "contact.html")

# ================== CHECKOUT =====================

@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in items)

    return render(request, "checkout.html", {
        "items": items,
        "total": total
    })



@login_required
def confirm_order(request):
    if request.method == "POST":
        items = Cart.objects.filter(user=request.user)
        if not items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect("cart")

        total = sum(item.subtotal() for item in items)

        payment_method = request.POST.get("payment_method")

        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            address=request.POST.get("address"),
            payment_method=payment_method,
            payment_status="Paid" if payment_method == "ONLINE" else "Pending",
            order_status="Placed"
        )

        # Save items
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                qty=item.qty,
                price=item.product.price
            )

        items.delete()  # clear cart

        if payment_method == "COD":
            return redirect("order_success", order_id=order.id)

        # Online Payment Test Page
        return redirect("payment_test", order_id=order.id)

    return redirect("checkout")
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order

def payment_test(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.payment_status = "Paid"
        order.save()
        return redirect("order_success", order_id=order.id)

    return render(request, "payment_test.html", {"order": order})

from .models import OrderItem

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = OrderItem.objects.filter(order=order)

    return render(request, "order_success.html", {
        "order": order,
        "items": items
    })

 #========================== Whislist========================
@login_required
def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    return redirect('wishlist')


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})


@login_required
def remove_from_wishlist(request, item_id):
    Wishlist.objects.filter(id=item_id, user=request.user).delete()
    return redirect('wishlist')

from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from .models import Order

#Payment Invoice
@login_required
def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Invoice_Order_{order.id}.pdf"'
    )

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, "E-Crochet Hub - Invoice")

    # Order Info
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 90, f"Order ID: {order.id}")
    p.drawString(50, height - 110, f"Customer: {order.full_name}")
    p.drawString(50, height - 130, f"Phone: {order.phone}")
    p.drawString(50, height - 150, f"Payment Method: {order.payment_method}")
    p.drawString(50, height - 170, f"Payment Status: {order.payment_status}")

    # Product list
    y = height - 220
    p.drawString(50, y, "Products:")
    y -= 20

    for item in order.items.all():
        p.drawString(
            60, y,
            f"{item.product.name}  x{item.qty}  ₹{item.price}"
        )
        y -= 20

    # Total
    y -= 20
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, f"Total Amount: ₹{order.total_amount}")

    p.showPage()
    p.save()

    return response
