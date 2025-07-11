from django.shortcuts import render

def no_permission(request):
    return render(request, 'no_permission.html')