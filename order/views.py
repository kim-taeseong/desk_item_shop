from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from logistics.models import Product
from .models import Order
from django.contrib.auth.decorators import login_required
from users.decorators import customer_required

@login_required(login_url='users:login')
@customer_required
def order(request):
    if request.method == 'POST':
        # 해당 제품 가져오기
        product = Product.objects.get(id=request.POST.get('product'))
        amount = int(request.POST.get('amount'))
        # 재고 비교
        # 주문한 수량 >= 재고
        if amount <= product.product_inventory:
            product.product_inventory -= amount
            product.save()
            price = product.product_price * amount
            address = request.user.customer.cus_address
            data, created = Order.objects.get_or_create(product=product, customer=request.user.customer, address=address, defaults={'amount': amount, 'price': price})
            if not created:
                data.amount += amount
                data.price += price
            data.save()
            return render(request, 'order/order.html', {'status': '주문이 완료되었습니다.'})
        # 주문한 수량 < 재고
        else:
            
            return render(request, 'order/order.html', {'status': '재고가 부족합니다.'})
        
def display_orders_history(request):
    orders = Order.objects.filter(customer=request.user.customer)
    context = {'orders': orders}
    return render(request, 'order/order_list.html', context)

def display_order(request, pk):
    # if request.user.is_authenticated
    order = Order.objects.get(id=pk)
    return HttpResponse(order)

def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('orders:display_orders')
    return render(request, 'order/order_delete.html', {'order': order})