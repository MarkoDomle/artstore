from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect

from artapp.forms import CustomerRegistrationForm, CustomAuthenticationForm, DeliveryInfoForm
from artapp.models import Picture, Cart, DeliveryInfo, Order


# Create your views here.


def index(request):
    pictures = Picture.objects.all()[:6]
    context = {"pictures": pictures}
    return render(request, "index.html", context)

def search(request):
    search_term = request.GET.get('search_term')
    pictures = Picture.objects.filter(title__icontains=search_term)[:6]
    context = {"pictures": pictures, "search_term": search_term}
    return render(request, 'index.html', context)

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_price = 0
    for item in cart_items:
        item.total_price = item.quantity * item.picture.price
        total_price += item.total_price

    return render(request, 'cart.html', {'cart_items': cart_items, "total": total_price})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Redirect to the login page after successful registration
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def add_to_cart(request, picture_id):
    if request.method == 'POST':
        picture = Picture.objects.get(id=picture_id)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = Cart.objects.get_or_create(user=request.user, picture=picture)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return redirect('/cart')


def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart')

def info(request):
    user = request.user
    delivery_info = None

    try:
        delivery_info = DeliveryInfo.objects.get(user=user)
        initial_data = {
            'name': delivery_info.name,
            'surname': delivery_info.surname,
            'address': delivery_info.address,
            'city': delivery_info.city,
            'country': delivery_info.country,
            'phone': delivery_info.phone,
        }
    except DeliveryInfo.DoesNotExist:
        initial_data = {}

    if request.method == 'POST':
        form = DeliveryInfoForm(request.POST)
        if form.is_valid():
            if delivery_info:
                delivery_info.name = form.cleaned_data['name']
                delivery_info.surname = form.cleaned_data['surname']
                delivery_info.address = form.cleaned_data['address']
                delivery_info.city = form.cleaned_data['city']
                delivery_info.country = form.cleaned_data['country']
                delivery_info.phone = form.cleaned_data['phone']
                delivery_info.save()
            else:
                delivery_info = DeliveryInfo.objects.create(
                    user=user,
                    name=form.cleaned_data['name'],
                    surname=form.cleaned_data['surname'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    country=form.cleaned_data['country'],
                    phone=form.cleaned_data['phone']
                )

            cart_items = Cart.objects.filter(user=user)
            total_price = 0
            for item in cart_items:
                item.total_price = item.quantity * item.picture.price
                total_price += item.total_price

            order = Order.objects.create(
                user=user,
                delivery_info=delivery_info,
                total_price=total_price
            )
            return redirect('/confirmed')
    else:
        form = DeliveryInfoForm(initial=initial_data)

    return render(request, 'deliveryinfo.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')



def confirmed(request):
    Cart.objects.filter(user=request.user).delete()
    return render(request, 'confirm.html')


