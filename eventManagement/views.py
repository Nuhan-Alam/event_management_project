from django.shortcuts import render, get_object_or_404, redirect

def redirect_to_home(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('sign-in')