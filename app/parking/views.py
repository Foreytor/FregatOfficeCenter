from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='login')
def index(request):

    context = {'bbs': 'dfg'}
    return render(request, "parking/index.html", context)

def indexf(request):

    context = {'bbs': 'dfg'}
    return render(request, "parking/index.html", context)
