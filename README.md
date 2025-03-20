# 分流系统

这是一个基于Python+Django Admin的Web版分流系统，使用MySQL作为数据库。

## 功能特点

- 用户登录认证
- Django Admin管理界面
- 分流规则管理
- 分流流量记录
- 两个自定义页面（当前为空白）

## 技术栈

- Python 3.8+
- Django 4.2.7
- MySQL
- Bootstrap 5

## 安装步骤

1. 克隆项目到本地

```bash
git clone https://github.com/yourusername/diversion_system.git
cd diversion_system
```

2. 创建虚拟环境并激活

```bash
python3 -m venv py_flxt
source py_flxt/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖包

```bash
pip3 install -r requirements.txt
```

4. 创建MySQL数据库

```sql
CREATE DATABASE diversion_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. 创建.env文件配置数据库连接（可选）

```
DB_NAME=diversion_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your_secret_key
DEBUG=True
```

6. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

7. 创建超级用户

```bash
python manage.py createsuperuser
```

8. 运行开发服务器

```bash
python manage.py runserver
```

9. 访问系统

- 网站首页：http://127.0.0.1:8000/
- 管理后台：http://127.0.0.1:8000/admin/

## 系统配置

系统的主要配置项在 `diversion_system/settings.py` 文件中，您可以根据需要进行修改。

## 使用说明

1. 登录系统
2. 在管理后台创建分流规则
3. 系统会根据规则对流量进行分流
4. 分流记录可在管理后台查看

## 生产环境部署建议

1. 使用Nginx + Gunicorn部署
2. 启用HTTPS
3. 关闭DEBUG模式
4. 使用环境变量设置敏感信息
5. 配置数据库连接池

## 许可证

MIT 