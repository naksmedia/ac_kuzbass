from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'mainapp/index.html')
def base(request):
    return render(request, 'mainapp/base.html')