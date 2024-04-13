from functools import wraps
from django.http import HttpResponseForbidden


def is_premium_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Premium member access required.")
    return wrapper
