from functools import wraps
from django.shortcuts import redirect

def custom_login_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if 'user_id' in request.session:  
            return function(request, *args, **kwargs)
        else:
            return redirect('login')  
    return wrap