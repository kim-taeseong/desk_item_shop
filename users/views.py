from django.shortcuts import render
from .forms import PurchaseForm

def product_detail(request, product_id):
    # 상품 상세 정보를 보여주는 뷰
    # product_id에 해당하는 상품 정보를 가져와서 템플릿에 전달
    return render(request, 'product_detail.html', {'product_id': product_id})

def purchase(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            # 폼이 유효한 경우 처리 로직 구현
            # 예: 주문 생성, 결제 진행 등
            return render(request, 'purchase_success.html')
    else:
        form = PurchaseForm()
    return render(request, 'purchase.html', {'form': form})