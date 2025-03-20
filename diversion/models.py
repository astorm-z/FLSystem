from django.db import models
from django.contrib.auth.models import User

class DivertedTraffic(models.Model):
    """流量分流记录模型"""
    source_ip = models.GenericIPAddressField(verbose_name="源IP地址")
    destination = models.CharField(max_length=255, verbose_name="目标位置")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="分流时间")
    user_agent = models.TextField(blank=True, null=True, verbose_name="用户代理")
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="处理人员")
    status = models.CharField(max_length=50, verbose_name="状态")
    
    class Meta:
        verbose_name = "分流记录"
        verbose_name_plural = "分流记录"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.source_ip} → {self.destination} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"


class DivertRule(models.Model):
    """分流规则模型"""
    name = models.CharField(max_length=100, verbose_name="规则名称")
    source_pattern = models.CharField(max_length=255, verbose_name="源匹配模式")
    destination = models.CharField(max_length=255, verbose_name="目标位置")
    priority = models.IntegerField(default=0, verbose_name="优先级")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_rules", verbose_name="创建人")
    
    class Meta:
        verbose_name = "分流规则"
        verbose_name_plural = "分流规则"
        ordering = ['-priority', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.source_pattern} → {self.destination})" 