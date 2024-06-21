from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def customer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users:login'):
    '''
    로그인한 유저가 고객인지 확인하는 데코레이터
    필요하다면 로그인 페이지로 이동
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_customer,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def store_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='users:login'):
    '''
    로그인한 유저가 판매자인지 확인하는 데코레이터
    필요하다면 로그인 페이지로 이동
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_active and u.is_store,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator