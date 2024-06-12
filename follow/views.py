from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from users.models import Customer

@login_required
def follow(request, user_id):
    user_to_follow = get_object_or_404(Customer, user_id=user_id)
    request.user.customer.follows.add(user_to_follow)
    return redirect('user_profile', user_id=user_id)

@login_required
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(Customer, user_id=user_id)
    request.user.customer.follows.remove(user_to_unfollow)
    return redirect('user_profile', user_id=user_id)

def user_profile_view(request, user_id):
    user_profile = get_object_or_404(Customer, user_id=user_id)
    context = {
        'user_profile': user_profile,
        'is_following': user_profile in request.user.customer.follows.all() if request.user.is_authenticated else False,
    }
    return render(request, 'follow/user_profile.html', context)
