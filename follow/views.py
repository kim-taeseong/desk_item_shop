from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from users.models import Customer
from users.decorators import customer_required

@customer_required
def follow_and_unfollow(request):
    user_id = request.POST.get('user_id')
    customer = get_object_or_404(Customer, user_id=user_id)
    if request.method == 'POST':
        if customer in request.user.customer.follows.all():
            request.user.customer.follows.remove(customer)
            return JsonResponse({
                    'message': 'Unfollow successfully!',
                    'check': False
            })
        else:
            request.user.customer.follows.add(customer)
            return JsonResponse({
                    'message': 'Follow successfully!',
                    'check': True
            })
    return JsonResponse({'message': 'Invalid request'}, status=400)