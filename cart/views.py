from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Cart
from django.db.models import Sum

class CartView(View):
    def get(self, request, *args, **kwargs):
        cart_id = kwargs.get('cart_id')
        cart_item = get_object_or_404(Cart, id=cart_id)
        return render(request, 'cart/cart_detail.html', {'cart': cart_item})

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        cart_id = kwargs.get('cart_id')
        cart_item = get_object_or_404(Cart, id=cart_id)
        
        if action == 'increase':
            cart_item.amount += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.amount > 1:
                cart_item.amount -= 1
                cart_item.save()
            else:
                cart_item.delete()
        return redirect('cart:cart_detail', cart_id=cart_id)

    def cart_detail(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total_quantity = cart_items.aggregate(total=Sum('amount'))['total'] or 0  # 장바구니에 담긴 총 수량

        context = {
            'cart_items': cart_items,
            'total_quantity': total_quantity,
        }
        return render(request, 'cart_detail.html', context)