# lib
Library Book Manager System Support By Python-Django

# 环境
Python2.7
Django

# 配置
在`setting.py`文件中配置localhost的mysql数据库地址及用户名密码

# 迁移项目
在项目根目录下执行如下代码

```python
python manage.py makemigrations library
python manage.py migrate
```

Django将自动创建项目所需的数据库表

# 运行

```python
    python manager.py runserver
```
默认在8000端口运行，可以访问 http://localhost:8000 查看运行结果

如果在接入外网服务器上使用这种运行方式，会导致外网无法访问的问题，使用如下命令可以保服务器自身和外网客户端都能访问该项目。

请自行把<port>替换成运行该项目的端口

```python
    python manage.py runserver 0.0.0.0:<PORT>
```

