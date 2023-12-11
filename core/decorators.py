from django.shortcuts import redirect

def manager_access(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_manager:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('/employeeDashboard/')
        return redirect('/')
    return wrapper