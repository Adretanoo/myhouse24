# Create your views here.
from django.shortcuts import render


def statistics(request):
    return render(request, "base_adminlte.html")
