from django.shortcuts import render, redirect
from .models import Customer, ShippingAddress, Product, Order, OrderItem

def create_order(request):
    if request.method == 'POST':
        # POST 요청에서 주문 관련 정보를 가져와서 처리합니다.
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        shipping_address = request.POST.get('shipping_address')
        shipping_postal_code = request.POST.get('shipping_postal_code')
        # 추가 필드들을 여기에 가져오세요.

        # 주문자 정보 생성
        customer = Customer.objects.create(name=customer_name, email=customer_email, phone_number=customer_phone)

        # 배송지 정보 생성
        shipping_address = ShippingAddress.objects.create(customer=customer, address=shipping_address, postal_code=shipping_postal_code)
        
        # 주문 정보 생성
        order = Order.objects.create(customer=customer, shipping_address=shipping_address)

        # 주문 상품 정보 생성
        # 여기서는 간단히 POST 데이터를 처리하지만, 실제로는 상품 목록을 받아와서 처리해야 합니다.
        product_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quantity')
        product = Product.objects.get(pk=product_id)
        OrderItem.objects.create(order=order, product=product, quantity=product_quantity)

        # 주문이 완료되면 홈페이지로 리다이렉트합니다. (원하는 페이지로 변경 가능)
        return redirect('/')
    else:
        # GET 요청인 경우, 주문 폼을 보여줍니다.
        return render(request, 'order_form.html')

def cancel_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    # 주문을 취소하는 로직을 작성하세요.
    order.delete()
    return redirect('/')
