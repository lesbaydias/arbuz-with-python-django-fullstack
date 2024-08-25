from django.shortcuts import redirect


def login_required(view_func, login_url='login'):
    def wrapper_func(request, *args, **kwargs):
        if not 'user' in request.session:
            return redirect(login_url)
        return view_func(request, *args, **kwargs)
    return wrapper_func


def is_admin(login_url='home'):
    def wrap(view_func):
        def wrapper_func(request, *args, **kwargs):
            user = request.user
            if not user.is_superuser:
                return redirect(login_url)
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return wrap


def apply_to_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate