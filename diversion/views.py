from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def page_one(request):
    """第一个空白页面"""
    context = {
        'page_title': '页面一'
    }
    return render(request, 'page_one.html', context)


@login_required
def page_two(request):
    """第二个空白页面"""
    context = {
        'page_title': '页面二'
    }
    return render(request, 'page_two.html', context)


@login_required
def home(request):
    """首页"""
    context = {
        'page_title': '分流系统首页'
    }
    return render(request, 'home.html', context) 