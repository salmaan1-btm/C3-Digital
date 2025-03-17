from django.shortcuts import render

# Create your views here.
def index(request):
    """The home page for C3 App 1."""
    return render(request, 'C3_app1/index.html')
