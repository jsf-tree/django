# [Django](https://docs.djangoproject.com/)
A popular Python framework for backend webdev, nowadays mostly used to build APIs that retrieve data, leaving the responsibility for serving HTML to the frontend.
Tutorials: [Overview of Django in 8 Mins](https://youtu.be/0sMtoedWaf0); [Mosh](https://youtu.be/rHux0gMZ3Eg) uses `pipenv` to manage envs &  dependencies;  
[Django Oficial Tutorial](https://docs.djangoproject.com/en/4.2/intro/): 2-[Models_dbAPI_AdminPage](https://docs.djangoproject.com/en/4.2/intro/tutorial02/), 3-[Views_Templates_Namespacing](https://docs.djangoproject.com/en/4.2/intro/tutorial03/), 4-[Forms_GenericViews](https://docs.djangoproject.com/en/4.2/intro/tutorial04/).

To start the server: `pipenv shell` and `python manage.py runserver <port-number>`  
_Scroll to the end for pipenv and django installation_

### Loose coupling philosophy
Django uses a main project (often named after setup or mysite) and several apps that plug to the project. This framework's philosophy follows loose coupling, meaning it provides ways to use an app in another projects. Because of this, each file has a clear responsibility.

![image](/img.svg "Flowchart")

### 1. Create a Project
`django-admin startproject setup .` creates a project called setup in the current directory with the **manage.py** (a wrapper¹ around `django-admin` that takes settings.py into account) and the default project folder with

| Default file     | Reponsibility                                                     |
| ---------------- | ----------------------------------------------------------------- |
| __init__.py      | defines this directory as a package                               |
| settings.py      | defines the app settings                                          |
| urls.py          | define urls of the application                                    |
| wsgi and asgi.py | used for deployment                                               |

When the server is run, it creates a `db.sqlite3` database if you have no database in your project.

Five commonly used commands in Django are:
```shell
# Creates boilerplate django files
django-admin startproject <project-name>

# Creates boilerplate of app folder and files
python manage.py startapp <app-name>

# Preps our database for migrations
python manage.py makemigrations

# Executes our migrations & updates the database
python manage.py migrate

# Creates a user with admin level permissions for the db
python manage.py createsuperuser
```

### 2. Create an App
Every Django Project is a collection of several apps, each app providing a certain functionality. 
In `settings.py` module, the INSTALLED_APPS keeps the registered apps.
Here are the default apps:
| Default installed apps      | Usage                                                   |
|-----------------------------|---------------------------------------------------------|
| django.contrib.admin        | admin interface for managing our data                   |
| django.contrib.auth         | authenticate users                                      |
| django.contrib.contenttypes | ...                                                     | 
| django.contrib.sessions     | temporary memory on the server for managing user's data |
| django.contrib.messages     | display one-time notifications to the user              |
| django.contrib.staticfiles  | serving static files to the user (images, css, etc)     |

To create the first app, open a new terminal, cd to where the "venv shell" is set 
(ie. where "Pipfile and Pipfile.lock" are), 
and run `python manage.py startapp myfirstapp`. 
This creates a folder (every Django app has the exact same structure):
| Default files | Usage                                                                                     |
|---------------|-------------------------------------------------------------------------------------------| 
| migrations    | generating database tables                                                                |
| admin         | how the admin interface for this app will look like                                       |
| apps          | where you configure the app                                                               |
| models        | define the model classes (which pull out data from the database and present to the user)  |
| tests         | define unit tests                                                                         |
| views         | request handlers                                                                          |

> Every new app must be registered in the setup settings modules, in the list of INSTALLED_APPS

### 3. [Views](https://docs.djangoproject.com/en/4.2/intro/tutorial03/), the public interface
Every data exchange involves a request and a response, which is achieved by protocols like HTTP. Views are the public interface, providing handlers (in the form of **functions** or **classes**) that connect user's requests coming through the endpoints in **urls.py** and perform actions like serving a html (**templates.py**) or interacting with the database (**models.py**). Effectively, views are request handlers (ie they handle the "request -> response" flow). Some frameworks call it an "action".

> Angle brackets “captures” part of the URL and sends it as a keyword argument to the view function. In `hello/<str:name>`, the part after "/" will get converted to "str" and stored to a var called "name", which will be used as a keyword in the view method.  

- **Views** stay under the respective app's **views.py**:
```python
from django.shortcuts import render
from django.http import HttpResponse


# Function-based view
def say_hello(request, name=''):
    return HttpResponse('Hello World %s' % name)

# Class-based view
class ProfileView(View):
    def get(self, request):
        user = getUser()
        # "<app_name>/" is how you can namespace your templates
        return render(request, '<app_name>/profile.html', {'user':user})
    def post(self, request):
        pass
```
- **URL routing** can be kept under the respective app's dir by creating **urls.py**:
```python
from django.urls import path
from . import views


# add name(space) for loose coupling
urlpatterns = [
    path('hello/', views.say_hello, name='without_name'),
    path('hello/<str:name>', views.say_hello, name='with_name'),
]
```

- Include each app **urls.py** in the projects's **urls.py** register:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<app_name>/', include('<app_name>.urls')),
]
```
#### 3+ [Generic Views](https://docs.djangoproject.com/en/4.2/intro/tutorial04/)
**Generic views** abstract common patterns to the point where you don’t even need to write Python code to write an app.


### 4. [Templates](https://docs.djangoproject.com/en/4.2/topics/templates/), the html
**Templates** are html files kept under the app's dir, like `<app_dir>/templates/<app_name>/index.html`.  
_Best Practice: the subfolder **app_name** namespaces the app templates and guarantees correctly  routing when the Project group all the app's template together._

The example of a template below shows the modular syntax:
```html
<!-- this is only an example, for serious projects write full html docs-->
{% if name %}
    <h1>Hello, {{ name }}!</h1>
{% else %}
    <h1>Hello, World!</h1>
{% endif %}
```
3. in views, add the request handler:
```python
def say_hello(request):
    return render(request, 'hello.html', context={'name': 'juliano'})
```

A solid understanding of the Django template language for html is useful:
```html
<!-- Variables in Django -->
{{ variable }}

<!-- Tags in Django -->
{% tag %}

<ul>
    {% for athelete in athlete_list %}
        <li>{{ athlete.name }} </li>
    {% endfor %}
</ul>    
```

### 5. [Models](), the database tables
They are class-based representations of our database table and constitute the core of database design in Django. They inherit from Django Models. Attributes represent the columns for the table. One can create relations between 1:1, n:1, and n:m. You can use an optional first positional argument to a Field to designate a human-readable name. 

It’s important to add __str__() methods to your models, not only for your own convenience when dealing with the interactive prompt, but also because objects’ representations are used throughout Django’s automatically-generated admin.

```python
class Product(models.Model):
    product_id = models.UUIDField()

class Project(models.Model):
    title = models.charField(max_length=255)
    description = models.TextField()
    uuid = models.UUIDField()
    pub_date = models.DateTimeField("date published")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
```

### 6. Debugging Django applications in VS Code
On the left panel, click on `Run and Debug` (Ctrl+Shift+D).  
Click on `create a launch.json file`, select Django.  
Set the key-value pairs accordingly.  
In configurations.args, one can add "9000" to void clash with the port 8000 where server is usually on for instance.  

The VS Code debugger works pretty similar to other debugs (Breakpoints, Step Over, Step In, Step Out)

### 6+. Django Debug Toolbar
--> [Reference](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html) <--  
Install it with `pipenv install django-debug-toolbar`  
Add `debug_toolbar` in the list of installed apps in the settings module.  
Add a new url entry to the `urlpatterns` in the main url module: `path('__debug__/', include(debug_toolbar.urls))` and add at the top `import debug_toolbar`.  
Add the middle ware `"debug_toolbar.middleware.DebugToolbarMiddleware"` at the top of MIDDLEWARE also in the settings module.  
Add the internal ip. For local development, also in the settings module, add:
```python
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
```
The toolbar only appears if a html document is being served. Within the toolbar, the SQL panel shows the queries called in the database. When querying the database using Djangos querying relational mapper, it generates queries and send to the database (here the generated queries can be seen).



### 7. Other functionalities in Django
#### 7.1 Django ORM
Django has a builtin ORM that helps working with the database. Here are a few the methods to retrieve data from the database via ORM:
```python
item = ModelName.objects.get(id=1)
querySet = ModelName.objects.all
quertSet = ModelName.objects.filter()
```

#### 7.2 Admin Panel
Quick start interface to work with our data. But a personal panel can be made.

#### 7.3 CRUD Methods (Copy, Read, Update, Delete)
While one can use the Admin Panel for it, a customized html page can also be made. Using methods like save() and delete(). Also, one can use Django Model Forms and/or Class-based views to handle these functionalities.

#### 7.4 [Static files](https://youtu.be/0sMtoedWaf0?t=297)
These are .css, .js and images that are part of the application. One must declare the STATIC_ROOT, MEDIA_ROOT in the settings module.
```
static/styles       
static/js           
static/images       
```

#### 7.5 [Authentication](https://youtu.be/0sMtoedWaf0?t=302)
Django offers builtin

#### 7.6 [Signals](https://youtu.be/0sMtoedWaf0?t=360)
Django offers ways to add event listeners that fire-off actions every time the event occurs. For instance, send an e-mail when a new user registers in the website.

### 8. Organizing Models in Apps
A Django project contains one or more apps; each app provides a specific piece of functionality.

#### Bad Example - Monolith
One way to organize is all functionality in a single app, distribute it in a pip and anyone can install it in their project via `pipenv install`. So, for instance, the next we deal with the same kind of app, we don't need to rewrite code. However, as a project grows, the single app might become bloated with too many views, too many modules. It becomes a `Monolith`. Similar like a controller with too many buttons that overwhelm the user.
- Store (Single app)
    - Product
    - Tag
    - Collection
    - Cart
    - CartItem
    - Order
    - OrderItem
    - Customer       

#### Even worse example - too many dependent   

Other way is to divide each functionality to an app. It is also a bad example because these apps are highly-dependent on each other
- Products
    - Product
    - Collection
    - Tag        
- Customers (managing customers)
    - Customer 
- Carts (shopping cart funcitonality)
    - Cart
    - CartItem
- Orders
    - Order
    - OrderItem

#### Good Example
This is the ideal and it follows the UNIX philosophy "`do one thing and do it well.`. 
Highly-related entities are kept together, maintaining the apps self-contained and with zero coupling. Good design has minimal coupling and high cohesion (focused in a specific functionality and includes everything needed to fulfill that piece of functionality).
- Store
    - Product
    - Collection
    - Cart
    - CartItem
    - Order
    - OrderItem
    - Customer    
- Tags
    - Tag
    - TaggesItem


## 🐘 PostgreSQL DB setup 🐘
### To install PostgreSQL with PostGIS in WSL
```shell
sudo apt update
sudo apt install postgresql postgresql-contrib postgis
sudo systemctl enable postgresql
sudo systemctl start postgresql

# "sudo service" is the older version of "sudo systemctl"
# "sudo service" does not have as advanced tooling as "sudo systemctl"
#  but it can start/stop/restart the services with
#      sudo service postgresql start/stop/restart
```

### Adjust PostgreSQL
Get a PostgreSQL server online;   
In PostgreSQL dir (on Debian/Ubuntu, it is `/etc/postgresql/<version>/main/`), adjust in `data/postgresql.conf` to `listen_addresses = '*'` and in `pg_hba.conf` to permit connections with `host all all 0.0.0.0/0 md5`.

Access it via psql (on Linux, `sudo -u postgres psql` -- change password with `ALTER USER postgres PASSWORD 'new_password';`). Once inside it, create there a database (eg db_w_postgis) with superuser django.  

Create a database with PostGIS
```SQL
CREATE DATABASE db_w_postgis;
\c db_w_postgis;
CREATE EXTENSION postgis;
```

Create a new user with specific permissions
```SQL
CREATE USER django WITH PASSWORD 'django';
GRANT CONNECT ON DATABASE db_w_postgis TO django;
GRANT USAGE ON SCHEMA public TO django;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO django;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO django;
```

For tests, **django** user must be able to create db: `ALTER USER django CREATEDB;`

### Adjust Django
Create a `.env` file and set the env variables; `pip install python-dotenv`; import it in **settings.py** and `dotenv.load_dotenv()`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_DEFAULT_NAME'),
        'USER': os.environ.get('DB_DEFAULT_USER'),
        'PASSWORD': os.environ.get('DB_DEFAULT_PASSWD'),
        'HOST': os.environ.get('DB_DEFAULT_HOST'),
        'PORT': os.environ.get('DB_DEFAULT_PORT'),
    }
}
```
Once the DB is set, 
- Adjust your app's **models.py**;
- Run `python manage.py makemigrations <app>` for each invididual app to create and store each individual app. (this commit to Django's version control)  
_To check the migration SQL, type `python manage.py sqlmigrate <app> <migration_id>` — the migration id of `app/migrations/0001_initial.py` is `0001`._
- Run `python manage.py migrate` to create all necessary tables defined in each respective **models.py** of the **INSTALLED_APPS** declared in **settings.py**.  


### The Database API
`python manage.py shell` activates python with the **settings.py**. Table-classes can be imported from models and instantiated. Their method `.save()` must be called to add it to the database. All registers in a table can be called via `<class>.objects.all()`. They can be filtered `<class>.objects.filter(an_attrib)`. Relationships are further available depending on the attribute type (eg string accepts `<str_attrib__endswith>=text, <str_attrib__startswith>=text`; datetime accepts `<dt_attrib__year>=a_year`; FK relationship attributes accept `<FJ>__attrib`.. This works as many levels deep as you want. There's no limit.

### Django Admin
newsroom, unified interface for site administrators to edit content, admin isnt intended to be used by site visitors.

An admin user must exist (if it does not, `python manage.py createsuperuser` — mine is "admin:senhasenha"). Run the server (`python manage.py runserver`) and log in **http://127.0.0.1:8000/admin/**.


#### [OPTIONAL] 
Update Python & get **pipenv**
```bash
# Update APT & upgrade Python3
sudo apt update
sudo apt upgrade python3

# Install pip3 + pipenv
sudo apt install python3-pip
pip3 install pipenv

# If "warning: scripts in '/home/<usr>/.local/bin' not in PATH",
#   add it with `export PATH="$HOME/.local/bin:$PATH"`  
#   and activate it
# `source ~/.bashrc` (bzw, ~/.bash_profile or ~/.zshrc — depending on your file)

# Install django and psycopg2¹ (to enable PostgreSQL connection) to the pipenv
pipenv install django psycopg2-binary django-debug-toolbar
#¹ normal psycopg continuously fail <https://github.com/pypa/pipenv/issues/3991>

# Activate the virtual environment
pipenv shell
```
Adjust integrated terminal in VS Code to the right venv interpreter
- Activate the venv with `pipenv shell`; run `pipenv --venv`; copy the path, adding "/bin/python" to it; insert it all as the new interperter in VS Code (ctrl+P, "> Python: Select interpreter")
- Now, `python manage.py runserver` should run the server.

> if it returns a SyntaxError "File "manage.py", line 17 ) from exec",  
this happens every now and then when VS Code fails to activate the venv for this project;  
 all you have to do is open a new terminal window