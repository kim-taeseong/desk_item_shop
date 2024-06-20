from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from logistics.models import Product
from .models import Cart, CartItem

def add_to_cart(request, item_id):
    item = get_object_or_404(Product, id=item_id)
    amount = int(request.POST.get('amount'))
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not created:
            cart_item.quantity += amount
        else:
            cart_item.quantity = amount
        cart_item.save()
    else:
        cart = request.session.get('cart', {})
        cart[str(item_id)] = cart.get(str(item_id), 0) + amount
        request.session['cart'] = cart
    return redirect(reverse('cart:cart_detail'))

def cart_detail(request):
    cart_items = []
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        for item in items:
            cart_items.append({
                'id': item.id,
                'item': item.item,
                'quantity': item.quantity,
                'quantity_price': item.quantity * round(item.item.product_price * (1 - item.item.product_sale * 0.01)),
                'sales_price': round(item.item.product_price * (1 - item.item.product_sale * 0.01))
            })
    else:
        session_cart = request.session.get('cart', {})
        for item_id, quantity in session_cart.items():
            item = get_object_or_404(Product, id=item_id)
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'quantity_price': quantity * round(item.product_price * (1 - item.product_sale * 0.01)),
                'sales_price': round(item.product_price * (1 - item.product_sale * 0.01))
            })
    total_price = sum(item['quantity_price'] for item in cart_items)
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

def remove_from_cart(request, item_id):
    item = get_object_or_404(Product, id=item_id)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, item=item)
        cart_item.delete()
    else:
        cart = request.session.get('cart')
        del cart[str(item_id)]
        request.session['cart'] = cart
    return redirect(reverse('cart:cart_detail'))

def transfer_session_cart_to_user(request, user):
    session_cart = request.session.get('cart', {})
    if not session_cart:
        return
    
    cart = Cart.objects.get(user=user)

    for item_id, quantity in session_cart.items():
        item = get_object_or_404(Product, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
        cart_item.quantity += quantity
        cart_item.save()

    del request.session['cart']

@require_POST
def update_cart_item(request):
    cart_item_id = request.POST.get('cart_item_id')
    quantity = request.POST.get('quantity')

    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({'success': True, 'quantity': cart_item.quantity})
