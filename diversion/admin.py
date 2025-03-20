from django.contrib import admin
from .models import DivertedTraffic, DivertRule

@admin.register(DivertedTraffic)
class DivertedTrafficAdmin(admin.ModelAdmin):
    list_display = ('source_ip', 'destination', 'timestamp', 'status', 'processed_by')
    list_filter = ('status', 'timestamp', 'processed_by')
    search_fields = ('source_ip', 'destination', 'user_agent')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'

@admin.register(DivertRule)
class DivertRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_pattern', 'destination', 'priority', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'created_by')
    search_fields = ('name', 'source_pattern', 'destination')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # 如果是新创建的对象
            obj.created_by = request.user
        super().save_model(request, obj, form, change) 