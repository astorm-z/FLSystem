from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # 链接管理
    path('links/', views.link_list, name='link_list'),
    path('links/add/', views.link_add, name='link_add'),
    path('links/edit/<int:pk>/', views.link_edit, name='link_edit'),
    path('links/delete/<int:pk>/', views.link_delete, name='link_delete'),
    
    # 工单管理
    path('workorders/', views.workorder_list, name='workorder_list'),
    path('workorders/add/', views.workorder_add, name='workorder_add'),
    path('workorders/edit/<int:pk>/', views.workorder_edit, name='workorder_edit'),
    path('workorders/delete/<int:pk>/', views.workorder_delete, name='workorder_delete'),
    
    # 号码管理
    path('numbers/', views.number_list, name='number_list'),
    path('numbers/add/', views.number_add, name='number_add'),
    path('numbers/edit/<int:pk>/', views.number_edit, name='number_edit'),
    path('numbers/delete/<int:pk>/', views.number_delete, name='number_delete'),
] 