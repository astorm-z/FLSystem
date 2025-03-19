from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Link, WorkOrder, Number


class CustomAuthenticationForm(AuthenticationForm):
    """自定义登录表单"""
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'})
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'})
    )


class LinkForm(forms.ModelForm):
    """链接表单"""
    class Meta:
        model = Link
        fields = ['workOrder', 'country', 'identifier', 'description', 'status']
        widgets = {
            'workOrder': forms.Select(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'identifier': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class WorkOrderForm(forms.ModelForm):
    """工单表单"""
    class Meta:
        model = WorkOrder
        fields = [
            'type', 'name', 'orderUrl', 'startTime', 'endTime', 
            'numType', 'allCount', 'ratio', 'orderAcct', 
            'orderPsw', 'numSize', 'status'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'orderUrl': forms.URLInput(attrs={'class': 'form-control'}),
            'startTime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'endTime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'numType': forms.NumberInput(attrs={'class': 'form-control'}),
            'allCount': forms.NumberInput(attrs={'class': 'form-control'}),
            'ratio': forms.NumberInput(attrs={'class': 'form-control'}),
            'orderAcct': forms.TextInput(attrs={'class': 'form-control'}),
            'orderPsw': forms.TextInput(attrs={'class': 'form-control'}),
            'numSize': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class NumberForm(forms.ModelForm):
    """号码表单"""
    class Meta:
        model = Number
        fields = ['workOrder', 'link', 'type', 'num', 'status']
        widgets = {
            'workOrder': forms.Select(attrs={'class': 'form-control'}),
            'link': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'num': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        } 