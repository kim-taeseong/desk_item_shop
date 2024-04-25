from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .models import Cart
from django.urls import reverse


class CartView(View):
    def get(self, request, *args, **kwargs):
        # 모든 장바구니 항목을 조회합니다.
        cart_items = Cart.objects.all()
        
        context = {
            'cart_items': cart_items,
        }
        return render(request, 'cart/cart_detail.html', context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        cart_item_id = request.POST.get('cart_item_id')  # 폼에서 전달된 cart_item_id를 가져옵니다.
        cart_item = get_object_or_404(Cart, id=cart_item_id)  # 특정 장바구니 항목을 찾습니다.
            
        if action == 'add_to_cart':
            new_cart_item = Cart.objects.create(product=cart_item.product, amount=1)
            new_cart_item.save()
            return redirect(reverse('cart:cart_detail', kwargs={'cart_id': new_cart_item.id}))
        
        elif action == 'increase':
            cart_item.amount += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.amount > 1:
                cart_item.amount -= 1
                cart_item.save()
            else:
                cart_item.delete()
        
        return redirect(reverse('cart:cart_detail', kwargs={'cart_id': cart_item_id}))

