"""
URL Configuration for diversion_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('diversion.urls')),
]

# 自定义Admin站点标题和头部
admin.site.site_header = '分流系统管理'
admin.site.site_title = '分流系统管理后台'
admin.site.index_title = '欢迎使用分流系统管理后台' 