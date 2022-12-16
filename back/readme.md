首先创建虚拟环境：

```shell

Conda create --name {项目名称} python=3.7
```

 

启用虚拟环境：

```
Conda activate {项目名称}
```

 

安装依赖：

```
Pip install -r requirements.txt
```

 

创建数据库相关命令：

```
Python manage.py makemigrations
```

 

```
Python manage.py migrate
```



运行：

```
python manage.py runserver
```

