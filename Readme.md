# vedios
https://www.bilibili.com/video/BV1AE41117Up?p=16

# create project
django-admin startproject myweb

# run project
python manage.py runserver 0.0.0.0:80

# 创建app(sales)
python manage.py startapp sales

# 生成默认数据库
python manage.py migrate

# 生成自创建数据库(ORM)
python manage.py makemigrations sales
python manage.py migrate

# 创建super user
python manage.py createsuperuser