from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users.models import Store, User
from .models import UserFavoriteStore

@login_required
def save_and_remove_store(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        store = get_object_or_404(Store, user=user)
        favorite, created = UserFavoriteStore.objects.get_or_create(customer=request.user.customer, store=store)
        if created:
            return JsonResponse({
                'message': 'Store saved successfully!',
                'check': True
            })
        else:
            favorite.delete()
            return JsonResponse({
                'message': 'Store removed successfully!',
                'check': False
            })
    return JsonResponse({'message': 'Invalid request'}, status=400)