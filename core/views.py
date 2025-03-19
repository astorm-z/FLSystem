from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden

from .models import Link, WorkOrder, Number, Announcement
from .forms import CustomAuthenticationForm, LinkForm, WorkOrderForm, NumberForm


def login_view(request):
    """登录视图"""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})


@login_required
def logout_view(request):
    """登出视图"""
    logout(request)
    return redirect('login')


@login_required
def home(request):
    """首页视图，显示公告"""
    announcements = Announcement.objects.filter(is_active=True)
    return render(request, 'core/home.html', {'announcements': announcements})


# 链接管理视图
@login_required
def link_list(request):
    """链接列表视图"""
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    links = Link.objects.filter(user=request.user)
    
    # 应用搜索过滤
    if query:
        links = links.filter(
            Q(identifier__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # 应用状态过滤
    if status_filter:
        links = links.filter(status=status_filter)
    
    # 分页
    paginator = Paginator(links.order_by('-id'), 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
    }
    
    return render(request, 'core/link_list.html', context)


@login_required
def link_add(request):
    """添加链接视图"""
    # 检查用户是否达到链接配额
    if Link.objects.filter(user=request.user).count() >= request.user.linkQuota:
        messages.error(request, "您已达到链接数量上限。")
        return redirect('link_list')
    
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            messages.success(request, "链接添加成功。")
            return redirect('link_list')
    else:
        form = LinkForm()
        # 限制可选工单为当前用户的工单
        form.fields['workOrder'].queryset = WorkOrder.objects.filter(user=request.user)
    
    return render(request, 'core/link_form.html', {'form': form, 'title': '添加链接'})


@login_required
def link_edit(request, pk):
    """编辑链接视图"""
    link = get_object_or_404(Link, pk=pk)
    
    # 验证用户是否有权限编辑该链接
    if link.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("您没有权限编辑此链接。")
    
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            messages.success(request, "链接更新成功。")
            return redirect('link_list')
    else:
        form = LinkForm(instance=link)
        # 限制可选工单为当前用户的工单
        form.fields['workOrder'].queryset = WorkOrder.objects.filter(user=request.user)
    
    return render(request, 'core/link_form.html', {'form': form, 'title': '编辑链接'})


@login_required
def link_delete(request, pk):
    """删除链接视图"""
    link = get_object_or_404(Link, pk=pk)
    
    # 验证用户是否有权限删除该链接
    if link.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("您没有权限删除此链接。")
    
    if request.method == 'POST':
        link.delete()
        messages.success(request, "链接删除成功。")
        return redirect('link_list')
    
    return render(request, 'core/link_confirm_delete.html', {'link': link})


# 工单管理视图
@login_required
def workorder_list(request):
    """工单列表视图"""
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    workorders = WorkOrder.objects.filter(user=request.user)
    
    # 应用搜索过滤
    if query:
        workorders = workorders.filter(
            Q(name__icontains=query) | 
            Q(orderAcct__icontains=query)
        )
    
    # 应用状态过滤
    if status_filter:
        workorders = workorders.filter(status=status_filter)
    
    # 分页
    paginator = Paginator(workorders.order_by('-id'), 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
    }
    
    return render(request, 'core/workorder_list.html', context)


@login_required
def workorder_add(request):
    """添加工单视图"""
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            workorder = form.save(commit=False)
            workorder.user = request.user
            workorder.save()
            messages.success(request, "工单添加成功。")
            return redirect('workorder_list')
    else:
        form = WorkOrderForm()
    
    return render(request, 'core/workorder_form.html', {'form': form, 'title': '添加工单'})


@login_required
def workorder_edit(request, pk):
    """编辑工单视图"""
    workorder = get_object_or_404(WorkOrder, pk=pk)
    
    # 验证用户是否有权限编辑该工单
    if workorder.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("您没有权限编辑此工单。")
    
    if request.method == 'POST':
        form = WorkOrderForm(request.POST, instance=workorder)
        if form.is_valid():
            form.save()
            messages.success(request, "工单更新成功。")
            return redirect('workorder_list')
    else:
        form = WorkOrderForm(instance=workorder)
    
    return render(request, 'core/workorder_form.html', {'form': form, 'title': '编辑工单'})


@login_required
def workorder_delete(request, pk):
    """删除工单视图"""
    workorder = get_object_or_404(WorkOrder, pk=pk)
    
    # 验证用户是否有权限删除该工单
    if workorder.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("您没有权限删除此工单。")
    
    if request.method == 'POST':
        workorder.delete()
        messages.success(request, "工单删除成功。")
        return redirect('workorder_list')
    
    return render(request, 'core/workorder_confirm_delete.html', {'workorder': workorder})


# 号码管理视图
@login_required
def number_list(request):
    """号码列表视图"""
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    numbers = Number.objects.filter(user=request.user)
    
    # 应用搜索过滤
    if query:
        numbers = numbers.filter(num__icontains=query)
    
    # 应用状态过滤
    if status_filter:
        numbers = numbers.filter(status=status_filter)
    
    # 分页
    paginator = Paginator(numbers.order_by('-id'), 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
    }
    
    return render(request, 'core/number_list.html', context)


@login_required
def number_add(request):
    """添加号码视图"""
    if request.method == 'POST':
        form = NumberForm(request.POST)
        if form.is_valid():
            number = form.save(commit=False)
            number.user = request.user
            number.save()
            messages.success(request, "号码添加成功。")
            return redirect('number_list')
    else:
        form = NumberForm()
        # 限制可选工单和链接为当前用户的
        form.fields['workOrder'].queryset = WorkOrder.objects.filter(user=request.user)
        form.fields['link'].queryset = Link.objects.filter(user=request.user)
    
    return render(request, 'core/number_form.html', {'form': form, 'title': '添加号码'})


@login_required
def number_edit(request, pk):
    """编辑号码视图"""
    number = get_object_or_404(Number, pk=pk)
    
    # 验证用户是否有权限编辑该号码
    if number.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("您没有权限编辑此号码。")
    
    if request.method == 'POST':
        form = NumberForm(request.POST, instance=number)
        if form.is_valid():
            form.save()
            messages.success(request, "号码更新成功。")
            return redirect('number_list')
    else:
        form = NumberForm(instance=number)
        # 限制可选工单和链接为当前用户的
        form.fields['workOrder'].queryset = WorkOrder.objects.filter(user=request.user)
        form.fields['link'].queryset = Link.objects.filter(user=request.user)
    
    return render(request, 'core/number_form.html', {'form': form, 'title': '编辑号码'})


@login_required
def number_delete(request, pk):
    """删除号码视图"""
    number = get_object_or_404(Number, pk=pk)
    
    # 验证用户是否有权限删除该号码
    if number.user != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("您没有权限删除此号码。")
    
    if request.method == 'POST':
        number.delete()
        messages.success(request, "号码删除成功。")
        return redirect('number_list')
    
    return render(request, 'core/number_confirm_delete.html', {'number': number}) 