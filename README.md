# Ecommerce
<br/>

## Setup
<br/>
<br/>

### setup mysql database with your database name, username and password 

'''python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
'''
<br/>

### Migrate database
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```
<br/>

### create super user to add products
```bash
$ python manage.py createsuperuser
```
<br/>

### run server
```bash
$ python manage.py runserver
```
<br/>

### ADD products as admin
'''python
http://127.0.0.1:8000/admin/
'''
<br/>

### Register as customer then it will redirect you to login 
'''python
http://127.0.0.1:8000/register/
'''
<br/>

### Attatch customer to user and order in admin dashboard
<br/>

### Then login as customer and it will redirect you to main page `store.html` to view product and add to cart

'''python
http://127.0.0.1:8000/login/
'''
<br/>

### API documantaion 
`https://app.swaggerhub.com/apis/MOHAMEDABDELALIM2A/JWT/0.1`