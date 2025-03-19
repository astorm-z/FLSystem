from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilter
from import_export.admin import ImportExportModelAdmin

from .models import User, Link, WorkOrder, Number, Announcement


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('name', 'level', 'linkQuota', 'createTime', 'outDateTime', 'is_active', 'is_staff')
    list_filter = ('level', 'is_active', 'is_staff', ('createTime', DateRangeFilter), ('outDateTime', DateRangeFilter))
    search_fields = ('name',)
    ordering = ('-createTime',)
    
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        (_('会员信息'), {'fields': ('level', 'linkQuota', 'outDateTime')}),
        (_('权限'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2', 'level', 'linkQuota', 'outDateTime')
        }),
    )
    
    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(Link)
class LinkAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'identifier', 'country', 'status', 'workOrder', 'created_at')
    list_filter = ('status', 'country', ('created_at', DateRangeFilter))
    search_fields = ('identifier', 'description', 'user__name')
    raw_id_fields = ('user', 'workOrder')
    list_editable = ('status',)
    list_per_page = 20
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "workOrder" and not request.user.is_superuser:
            kwargs["queryset"] = WorkOrder.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:  # 如果是创建新记录
            if not request.user.is_superuser:
                obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(WorkOrder)
class WorkOrderAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'name', 'type', 'status', 'currentCount', 'allCount', 'startTime', 'endTime')
    list_filter = ('status', 'type', ('startTime', DateRangeFilter), ('endTime', DateRangeFilter))
    search_fields = ('name', 'orderAcct', 'user__name')
    raw_id_fields = ('user',)
    list_editable = ('status',)
    list_per_page = 20
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            if not request.user.is_superuser:
                obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Number)
class NumberAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'num', 'type', 'visitCount', 'validCount', 'status', 'workOrder', 'link')
    list_filter = ('status', 'type', ('created_at', DateRangeFilter))
    search_fields = ('num', 'user__name')
    raw_id_fields = ('user', 'workOrder', 'link')
    list_editable = ('status',)
    list_per_page = 20
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "workOrder":
                kwargs["queryset"] = WorkOrder.objects.filter(user=request.user)
            elif db_field.name == "link":
                kwargs["queryset"] = Link.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def save_model(self, request, obj, form, change):
        if not change:
            if not request.user.is_superuser:
                obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', ('created_at', DateRangeFilter))
    search_fields = ('title', 'content')
    list_editable = ('is_active',) 