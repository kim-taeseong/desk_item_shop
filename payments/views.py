# payments/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse, Http404
from .models import Payment, Order
import requests
import logging
from django.conf import settings
from logistics.models import Product
from users.models import Customer
from django.views.decorators.http import require_http_methods
import uuid
import json

logger = logging.getLogger(__name__)

def create_order(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        customer = get_object_or_404(Customer, user=request.user)
        
        amount = int(request.POST.get('amount'))
        price = product.product_price * amount
        
        order = Order.objects.create(product=product, customer=customer, amount=amount, price=price)
        
        # 고유한 orderNo 생성 (desk 접두사 추가)
        order_no = f"desk{order.id}"
        
        external_base_url = settings.EXTERNAL_BASE_URL
        result_callback_url = f"{external_base_url}{reverse('payments:callback')}"
        
        toss_payment_data = {
            "orderNo": order_no,
            "amount": price,
            "amountTaxFree": 0,
            "productDesc": product.product_name,
            "apiKey": settings.TOSS_API_KEY,
            "autoExecute": True,
            "resultCallback": result_callback_url,
            "callbackVersion": "V2",
            "retUrl": f"{external_base_url}{reverse('payments:success')}",
            "retCancelUrl": f"{external_base_url}{reverse('payments:error')}"
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        logger.info(f"Toss payment data: {toss_payment_data}")
        
        toss_response = requests.post("https://pay.toss.im/api/v2/payments", json=toss_payment_data, headers=headers)
        toss_response_data = toss_response.json()
        
        logger.info(f"Toss response data: {toss_response_data}")

        # 응답 데이터 출력
        print(json.dumps(toss_response_data, indent=4))
        
        if toss_response.status_code == 200:
            pay_url = toss_response_data.get('checkoutPage')
            if pay_url:
                return redirect(pay_url)
            else:
                error_msg = toss_response_data.get('msg', 'payUrl not found in the response')
                logger.error(f"Toss API error: {error_msg}")
                return render(request, 'payments/error.html', {'error': error_msg})
        else:
            error_msg = toss_response_data.get('msg', 'Unknown error')
            logger.error(f"Toss API error: {error_msg}")
            return render(request, 'payments/error.html', {'error': error_msg})
    
    else:
        product = get_object_or_404(Product, id=product_id)
        return render(request, 'payments/create_order.html', {'product': product})

def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    store_name = order.product.store.store_name
    amount = order.price
    
    payment = Payment.objects.create(
        order=order,
        name=store_name,
        amount=amount
    )

    # 고유한 order_no 생성 (desk 접두사 추가)
    order_no = f"desk{order.id}"
    
    external_base_url = settings.EXTERNAL_BASE_URL
    result_callback_url = f"{external_base_url}{reverse('payments:callback')}"
    
    toss_payment_data = {
        "orderNo": order_no,
        "amount": amount,
        "amountTaxFree": 0,
        "productDesc": order.product.product_name,
        "apiKey": settings.TOSS_API_KEY,
        "autoExecute": True,
        "resultCallback": result_callback_url,
        "callbackVersion": "V2",
        "retUrl": f"{external_base_url}{reverse('payments:success')}",
        "retCancelUrl": f"{external_base_url}{reverse('payments:error')}"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    logger.info(f"Toss payment data: {toss_payment_data}")
    
    toss_response = requests.post("https://pay.toss.im/api/v2/payments", json=toss_payment_data, headers=headers)
    toss_response_data = toss_response.json()
    
    logger.info(f"Toss response data: {toss_response_data}")

    # 응답 데이터 출력
    print(json.dumps(toss_response_data, indent=4))
    
    if toss_response.status_code == 200:
        pay_url = toss_response_data.get('checkoutPage')
        if pay_url:
            return redirect(pay_url)
        else:
            error_msg = toss_response_data.get('msg', 'payUrl not found in the response')
            logger.error(f"Toss API error: {error_msg}")
            return render(request, 'payments/error.html', {'error': error_msg})
    else:
        error_msg = toss_response_data.get('msg', 'Unknown error')
        logger.error(f"Toss API error: {error_msg}")
        return render(request, 'payments/error.html', {'error': error_msg})

def success(request):
    return render(request, 'payments/success.html')

def error(request):
    return render(request, 'payments/error.html')

@require_http_methods(["POST"])
def create_payment(request):
    try:
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        name = request.POST.get('name')
        amount = request.POST.get('amount')

        payment = Payment.objects.create(order=order, name=name, amount=amount)
        return JsonResponse({"merchant_uid": payment.merchant_uid, "status": payment.status})
    except Exception as e:
        logger.error(str(e), exc_info=e)
        return JsonResponse({"error": str(e)}, status=400)

@require_http_methods(["POST"])
def verify_payment(request, payment_id):
    try:
        payment = get_object_or_404(Payment, id=payment_id)
        payment.verify()
        return JsonResponse({"status": payment.status, "is_paid": payment.is_paid})
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        logger.error(str(e), exc_info=e)
        return JsonResponse({"error": str(e)}, status=400)

@require_http_methods(["POST"])
def cancel_payment(request, payment_id):
    try:
        api_key = settings.TOSS_API_KEY
        payment = get_object_or_404(Payment, id=payment_id)
        
        url = f"https://api.tosspayments.com/v1/payments/{payment.merchant_uid}/cancel"
        headers = {
            "Authorization": f"Basic {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            payment.status = 'cancelled'
            payment.is_paid = False
            payment.save()
            return JsonResponse({"status": payment.status, "is_paid": payment.is_paid})
        else:
            logger.error(f"Toss API error: {response_data}")
            return JsonResponse({"error": response_data}, status=response.status_code)
    except Http404 as e:
        return JsonResponse({"error": str(e)}, status=404)
    except Exception as e:
        logger.error(str(e), exc_info=e)
        return JsonResponse({"error": str(e)}, status=400)

def callback(request):
    # 결제 결과를 처리하는 로직을 여기에 추가합니다.
    return JsonResponse({"status": "callback received"})