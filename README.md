# 分流系统 (Traffic Distribution System)

这是一个基于Django Admin的分流系统，使用SQLite作为轻量级数据库。

## 功能模块

系统主要包含三大模块：
1. 链接管理
2. 工单管理 
3. 号码管理

## 安装步骤

1. 克隆仓库到本地
2. 创建虚拟环境：
```
python -m venv venv
```
3. 激活虚拟环境：
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. 安装依赖：
```
pip install -r requirements.txt
```
5. 运行数据库迁移：
```
python manage.py makemigrations
python manage.py migrate
```
6. 创建超级用户：
```
python manage.py createsuperuser
```
7. 启动服务器：
```
python manage.py runserver
```
8. 访问 http://127.0.0.1:8000/ 使用系统

## 开发者信息

本系统基于Python 3.8+和Django 4.2构建 

mkdir static 