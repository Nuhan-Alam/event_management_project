from django.shortcuts import render

def no_permission(request):
    return render(request, 'no_permission.html')

def intro(request):
    return render(request, "intro.html")