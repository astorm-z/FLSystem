from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError('用户名是必填字段')
        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('level', 9)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须将is_staff设置为True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须将is_superuser设置为True')
        
        return self.create_user(name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """用户模型"""
    name = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    outDateTime = models.DateTimeField(default=timezone.now, verbose_name='会员过期时间')
    level = models.IntegerField(default=1, verbose_name='会员等级')
    linkQuota = models.IntegerField(default=10, verbose_name='链接数量额度')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    is_staff = models.BooleanField(default=False, verbose_name='是否管理员')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'
        
    def __str__(self):
        return self.name
    
    @property
    def is_expired(self):
        """检查会员是否已过期"""
        return timezone.now() > self.outDateTime


class WorkOrder(models.Model):
    """工单模型"""
    TYPE_CHOICES = [
        (1, '类型1'),
        (2, '类型2'),
        (3, '类型3'),
    ]
    
    STATUS_CHOICES = [
        (0, '停用'),
        (1, '启用'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='work_orders')
    id = models.AutoField(primary_key=True, verbose_name='工单ID')
    type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name='工单类型')
    name = models.CharField(max_length=255, verbose_name='工单名称')
    orderUrl = models.URLField(verbose_name='工单URL')
    startTime = models.DateTimeField(verbose_name='开始时间')
    endTime = models.DateTimeField(verbose_name='结束时间')
    numType = models.IntegerField(default=1, verbose_name='号码类型')
    allCount = models.IntegerField(default=0, verbose_name='工单总量')
    currentCount = models.IntegerField(default=0, verbose_name='当前完成量')
    ratio = models.IntegerField(default=100, verbose_name='下号比率')
    orderAcct = models.CharField(max_length=100, verbose_name='工单账号')
    orderPsw = models.CharField(max_length=100, verbose_name='工单密码')
    numSize = models.IntegerField(default=0, verbose_name='号码数量')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='工单状态')
    
    class Meta:
        verbose_name = '工单'
        verbose_name_plural = '工单管理'
        
    def __str__(self):
        return self.name


class Link(models.Model):
    """链接模型"""
    STATUS_CHOICES = [
        (0, '停用'),
        (1, '启用'),
    ]
    
    COUNTRY_CHOICES = [
        ('CN', '中国'),
        ('US', '美国'),
        ('JP', '日本'),
        ('KR', '韩国'),
        ('UK', '英国'),
        # 更多国家可以在这里添加
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='links')
    workOrder = models.ForeignKey(
        WorkOrder, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='关联工单',
        related_name='links'
    )
    id = models.AutoField(primary_key=True, verbose_name='链接ID')
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, verbose_name='投放国家')
    identifier = models.CharField(max_length=255, unique=True, verbose_name='分流链接标识')
    description = models.TextField(blank=True, verbose_name='链接描述')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '链接'
        verbose_name_plural = '链接管理'
        
    def __str__(self):
        return self.identifier


class Number(models.Model):
    """号码模型"""
    STATUS_CHOICES = [
        (0, '停用'),
        (1, '启用'),
    ]
    
    TYPE_CHOICES = [
        (1, '类型1'),
        (2, '类型2'),
        (3, '类型3'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', related_name='numbers')
    workOrder = models.ForeignKey(
        WorkOrder, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='关联工单',
        related_name='numbers'
    )
    link = models.ForeignKey(
        Link, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='关联链接',
        related_name='numbers'
    )
    id = models.AutoField(primary_key=True, verbose_name='号码ID')
    type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name='号码类型')
    num = models.CharField(max_length=50, verbose_name='号码')
    visitCount = models.IntegerField(default=0, verbose_name='访问次数')
    validCount = models.IntegerField(default=0, verbose_name='进线次数')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '号码'
        verbose_name_plural = '号码管理'
        
    def __str__(self):
        return self.num


class Announcement(models.Model):
    """公告模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告管理'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title 