from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from logistics.models import Product
from .models import Order

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
            order = Order(product=product, customer=request.user.customer, amount=amount, price=product.product_price, address=request.user.customer.cus_address)
            order.save()
            return render(request, 'order/order.html', {'status': 'success'})
        # 주문한 수량 < 재고
        else:
            
            return render(request, 'order/order.html', {'status': '재고가 부족합니다.'})
        
def display_orders_history(request):
    orders = Order.objects.filter(customer=request.user.customer)
    result = list(orders.values())
    return JsonResponse(result, safe=False)

def display_order(request, pk):
    # if request.user.is_authenticated
    order = Order.objects.get(id=pk)
    return HttpResponse(order)

def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        order.delete()
        return HttpResponse('ok')
    return HttpResponse('ok')