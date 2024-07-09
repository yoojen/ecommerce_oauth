from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from .models import User


def is_not_admin(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        if request.user.is_superuser:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return func(request, *args, **kwargs)
    return wrapper

def is_admin(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        if not request.user.is_superuser:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return func(request, *args, **kwargs)
    return wrapper


def has_placed_order(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        try:
            user = request.user
            orders = user.order
            return func(request, *args, **kwargs)
        except User.order.RelatedObjectDoesNotExist:
            messages.info(request, "Please place order before you continue")
            return redirect(settings.LOGIN_REDIRECT_URL)
    return wrapper
