# [Django](https://docs.djangoproject.com/)
A popular Python framework for backend webdev, nowadays mostly used to build APIs that retrieve data, leaving the responsibility for serving HTML to the frontend.  
Tutorials: [Overview of Django in 8 Mins](https://youtu.be/0sMtoedWaf0); [Mosh](https://youtu.be/rHux0gMZ3Eg) uses `pipenv` to manage envs &  dependencies;  
[Django Oficial Tutorial](https://docs.djangoproject.com/en/4.2/intro/): 2-[Models_dbAPI_AdminPage](https://docs.djangoproject.com/en/4.2/intro/tutorial02/), 3-[Views_Templates_Namespacing](https://docs.djangoproject.com/en/4.2/intro/tutorial03/), 4-[Forms_GenericViews](https://docs.djangoproject.com/en/4.2/intro/tutorial04/).

```shell
pipenv shell  # Django & pipenv installation at the end
python manage.py runserver <port-number>
```

### Loose coupling philosophy
Django has a main project (often named setup/config/mysite) and a collection of plugable apps for each functionality, which can be reused in other projects.

![image](/img.svg "Flowchart")

### 1. Create a Project
"`django-admin startproject <project_name> .`" creates the boilerplate project in current dir with default files and **manage.py** (a wrapper¹ around `django-admin` that takes settings.py into account): . The default files are **wsgi.py** & **asgi.py** (for deployment), **urls.py** (for endpoint routing) and **settings.py**, in which configurations are set, like **INSTALLED_APPS** to keep the registered apps within the project:

| Default installed apps      | Usage                                                   |
|-----------------------------|---------------------------------------------------------|
| django.contrib.admin        | admin interface for managing our data                   |
| django.contrib.auth         | authenticate users                                      |
| django.contrib.contenttypes | ...                                                     | 
| django.contrib.sessions     | temporary memory on the server for managing user's data |
| django.contrib.messages     | display one-time notifications to the user              |
| django.contrib.staticfiles  | serving static files to the user (images, css, etc)     |

> If no database is set, Django creates a `db.sqlite3` db on the first run.

### 2. Create an App
"`python manage.py startapp <app-name>`" creates the boilerplate app 
| Default files | Usage                                                                                     |
|---------------|----------------------------------| 
| migrations    | generating database tables       |
| admin         | set up the app's admin interface |
| apps          | where you configure the app      |
| models        | define database tables           |
| tests         | define unit tests                |
| views         | request-response handlers        |

> Apps must be registered in **INSTALLED_APPS** under project's settings.py 


### 3. [Views](https://docs.djangoproject.com/en/4.2/topics/http/views/), the public interface ([Tutorial 03](https://docs.djangoproject.com/en/4.2/intro/tutorial03/))
Views are Request-Response HTTP handlers (in the form of **functions** or **classes**) connecting the endpoints (**urls.py**) to actions like serving a html (**templates.py**) or interacting with the database (**models.py**).

- **Views** are in `app_name/views.py`
```python
from django.http import HttpResponse
from django.shortcuts import render

# Function-based view
def say_hello(request, name=''):
    return HttpResponse('Hello World %s' % name)

# Class-based view
class ProfileView(View):
    def get(self, request):
        user = getUser()
        # the template "profile.html" is namespaced with "app_name"
        return render(request, 'app_name/profile.html', {'user':user})
    def post(self, request):
        pass
```

- **Endpoints & URL routing** are in `app_name/urls.py`:
```python
from django.urls import path
from . import views

app_name = 'app_name'  # namespacing
urlpatterns = [
    path('', views.say_hello, name='without_name'),

    # Angle brackets “captures” part of the URL and send it as a keyword arg to the view function. In `app_name/<str:name>`, the part after "/" converts to "str",  stores in a var called "name" and is passed to the view.
    path('<str:name>/', views.say_hello, name='with_name'),
]
```

- Include each app **urls.py** in the projects's **urls.py** register:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app_name/', include('app_name.urls')),
]
```  

Django also offers [Generic Views](https://docs.djangoproject.com/en/4.2/intro/tutorial04/) which are common patterns of views to quickly write an app.

### 4. [Templates](https://docs.djangoproject.com/en/4.2/topics/templates/), the html
**Templates** are HTML files served by views. They are kept inside a namespaced template folder following the format: `<app_dir>/templates/<app_name>/index.html`.  
> Best Practice: the subfolder **app_name** in **templates** namespaces the app templates and guarantees correctly  routing when the Project groups all the app's templates together. This way, different index.html will be recognizable: `<app_name1>/index.html` and `<app_name2>/index.html`  

Django Template syntax supports IO (context) and loops:
```html
<!-- this is only an example, for serious projects write full html docs-->
{% if name %}
    <h1>Hello, {{ name }}!</h1>
{% else %}
    <h1>Hello, World!</h1>
{% endif %}
```
The caller view would send "name" as  context:
```python
def say_hello(request):
    return render(request, 'hello.html', context={'name': 'juliano'})
```

A solid understanding of the Django template language for HTML is useful:
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

### [Static files](https://docs.djangoproject.com/en/4.2/howto/static-files/): further customization  [tutorial 6](https://docs.djangoproject.com/en/4.2/intro/tutorial06/)
Create a namespaced dir `<app_name>/static/<app_name>/` to keep JS, CSS and image files. Templates require `{% load static %}` at the top to generate the absolute URL to static files and the link  
 `<link rel="stylesheet" href="{% static 'polls/style.css' %}">`
 While the [default staticfiles app](https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/), a more robust & secure approach is needed in production: [staticfiles in production](https://docs.djangoproject.com/en/4.2/howto/static-files/deployment/).

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

#### 7.2 [Admin](https://docs.djangoproject.com/en/4.2/ref/contrib/admin/) Panel [tutorial 7](https://docs.djangoproject.com/en/4.2/intro/tutorial07/)
It creates an interface to work with your data (models). Each app must enable the admin interface or its model in its `<app_name>/admin.py`. The admin interface for each model can be customized and a model's admin interface can operate with other models for the case they have FK to other models (StackedInline and TabularInlline are two options).
```python
from django.contrib import admin
from .models import Question # 🌳 Tell Django that Question has an Admin Interface

# Default interface
admin.site.register(Question)

# Change default: create a Model Admin Class & pass it as 2nd arg to admin.site.register()

class ChoiceInline(admin.StackedInline):
    # Stacked FK subinterface, default 3
    model = Choice
    extra = 3

class ChoiceInline(admin.TabularInline):
    # Tabular FK subinterface, default 3
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    # Group fields in sets
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    # Change the list display (attributes and methods are possible)
    list_display = ["question_text", "pub_date", "was_published_recently"]
    # Adds a filter sidebar
    list_filter = ["pub_date"]
    # Add search functionality
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)
```

The Admin template itself can be customized.
Create a "templates" folder in project root directory (where manage.py is) and add a DIRS option in TEMPLATES setting.



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
Alternatively,
```shell
# Creates a user with admin level permissions for the db
python manage.py createsuperuser
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

### The Django test client
Django provides a test **Client** to simulate a user interacting with the code at the view level either via `python manage.py shell` or **views.py**.
```python
>>> from django.test.utils import setup_test_environment

# Install the template renderer to examine additional attrib on responses
# such as response.context
# Make sure you have TIME_ZONE set in settings.py before continuing
>>> setup_test_environment()
>>> from django.test import Client
>>> client = Client()

# Simulate the Client trying an URL
>>> response = client.get("/")
>>> response.status_code        # Check status_code

# One can also use namespaces via reverse to avoid hardcoding
>>> from django.urls import reverse
>>> response = client.get(reverse("polls:index"))
>>> response.content # Check content
>>> response.context["latest_question_list"] # Check context
```
In **views.py** we added `def queryset(self)` to the generic views so that they return questions that are not in the future. Furthermore, we added two test classes in **test.py** , one for each type of generic view.

When testting, more is better. Good rules-of-thumb are:
- a separate TestClass for each model or view
- a separate test method for each set of conditions you want to test
- test method names that describe their function

---


---

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