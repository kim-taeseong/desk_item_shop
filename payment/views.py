from django.shortcuts import render
from django.http import HttpResponse
from .models import Order, Payment

def create_order(request):
    if request.method == 'POST':
        order_data = {
            'order_number': request.POST.get('order_number'),
            'customer_name': request.POST.get('customer_name'),
            # 다른 필드도 필요한 경우 여기에 추가
        }
        order = Order.objects.create(**order_data)
        return HttpResponse("Order created successfully!")
    else:
        return render(request, 'create_order.html')

def process_payment(request):
    if request.method == 'POST':
        payment_data = {
            'order': request.POST.get('order'),
            'payment_method': request.POST.get('payment_method'),
            'amount': request.POST.get('amount'),
            # 다른 필드도 필요한 경우 여기에 추가
        }
        payment = Payment.objects.create(**payment_data)
        return HttpResponse("Payment processed successfully!")
    else:
        return render(request, 'process_payment.html')
