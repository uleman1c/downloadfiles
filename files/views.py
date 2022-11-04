from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def files(request, slug):

    d = 1

    # return HttpResponse(slug)
    return redirect('http://localhost:8008/el?id=' + slug)