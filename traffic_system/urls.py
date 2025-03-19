"""
URL configuration for traffic_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 自定义管理站点
admin.site.site_header = '分流系统管理后台'  
admin.site.site_title = '分流系统'
admin.site.index_title = '管理面板' 