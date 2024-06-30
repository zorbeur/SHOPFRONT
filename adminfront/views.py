from django.shortcuts import render

def Admin_home(request):
    return render(request, 'admin_index.html')


def admin_index(request):
    return render(request, 'admin_index.html')