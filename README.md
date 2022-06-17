# Authentication and Permissions II

Show students file management in templates

## What are the objectives?

- Understand how to make registration views
- Understand how to make login and logout views

## Pre-requisites

1. Clone this repo.
2. Create a virtual environment.
3. Install the deps using `pip install -r requirements/dev.lock`.

## Steps

### Registration

1. Add the registration form in `users/forms.py`:

   ```python
   from django import forms
   from django.contrib.auth import get_user_model


   User = get_user_model()


   class UserRegister(forms.ModelForm):
       class Meta:
           model = User
           fields = ["username", "first_name", "last_name", "email", "password"]

           widgets = {
               "password": forms.PasswordInput(),
           }
   ```

   - Explain that `User = get_user_model()` is so that we get the correct `User` model, regardless of whether it is the default user model or a custom made one (we have a custom user model in the same app).
   - The widget is so that the password does not appear when typed by the user.

2. Create the `registration` view in `users/views.py`:

   ```python
   from django.contrib.auth import login
   from django.shortcuts import render, redirect

   from users.forms import UserRegister


   def register_user(request):
       form = UserRegister()
       if request.method == "POST":
           form = UserRegister(request.POST)
           if form.is_valid():
               user = form.save(commit=False)

               user.set_password(user.password)
               user.save()

               login(request, user)
               return redirect("home")
       context = {
           "form": form,
       }
       return render(request, "register.html", context)
   ```

   - Explain that we use `commit=False` so that we can update the password before actually saving to the database.

3. Add our view to `urls.py`:

   ```python
   ...
   from users import views as user_views

   urlpatterns = [
       ...
       path("register/", user_views.register_user, name="register"),
   ]
   ```

4. Add the registration template in `users/templates/register.html`:

   ```html
   <!DOCTYPE html>
   {% load crispy_forms_tags %}
   <html lang="en">
     <head>
       <meta charset="UTF-8" />
       <meta http-equiv="X-UA-Compatible" content="IE=edge" />
       <meta name="viewport" content="width=device-width, initial-scale=1.0" />
       <title>Register</title>
       <link
         rel="stylesheet"
         href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"
         integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn"
         crossorigin="anonymous"
       />
     </head>
     <body>
       <nav class="navbar navbar-expand-lg navbar-light bg-light">
         <a class="navbar-brand" href="{% url 'home' %}">Bookstore</a>
         <button
           class="navbar-toggler"
           type="button"
           data-toggle="collapse"
           data-target="#navbarSupportedContent"
           aria-controls="navbarSupportedContent"
           aria-expanded="false"
           aria-label="Toggle navigation"
         >
           <span class="navbar-toggler-icon"></span>
         </button>

         <div class="collapse navbar-collapse" id="navbarSupportedContent">
           <ul class="navbar-nav mr-auto">
             <li class="nav-item active">
               <a class="nav-link" href="{% url 'home' %}">
                 Home <span class="sr-only">(current)</span>
               </a>
             </li>
             <li class="nav-item">
               <a class="nav-link" href="{% url 'register' %}">Sign Up</a>
               <a class="nav-link" href="">Sign In</a>
             </li>
           </ul>
         </div>
       </nav>

       <div class="container">
         <h1>Sign Up</h1>
         <form action="{% url 'register' %}" method="post">
           <!-- prettier-ignore -->
           {% csrf_token %}
           {{ form | crispy }}
           <button class="btn btn-success" type="submit">Sign Up</button>
         </form>
       </div>
     </body>
   </html>
   ```

5. Update your `home.html` template in `shared/templates` to include the `register` link in the navbar:

   ```html
   <a class="nav-link" href="{% url 'register' %}">Sign Up</a>
   ```

### Logout

1. Add the `logout` view in `users/views.py`:

   ```python
   from django.contrib.auth import login, logout

   ...

   def logout_user(request):
       logout(request)
       return redirect("home")
   ```

   - Explain that no form is needed

2. Add the `logout` view in `urls.py`:

   ```python
   ...

   urlpatterns = [
       ...
       path("logout/", user_views.logout_user, name="logout"),
   ]
   ```

3. Add the `logout` to our navbars like so:

   ```html
   <div class="collapse navbar-collapse" id="navbarSupportedContent">
     <ul class="navbar-nav mr-auto">
       <li class="nav-item active">
         <a class="nav-link" href="{% url 'home' %}">
           Home <span class="sr-only">(current)</span>
         </a>
       </li>
       {% if not user.is_authenticated %}
       <li class="nav-item">
         <a class="nav-link" href="{% url 'register' %}">Sign Up</a>
       </li>
       {% else %}
       <li>
         <a class="nav-link" href="{% url 'logout' %}">Log Out</a>
       </li>
       {% endif %}
     </ul>
   </div>
   ```

### Login

1. Add the login form in `users/forms.py`:

   ```python
   class UserLogin(forms.Form):
       username = forms.CharField(required=True)
       password = forms.CharField(required=True, widget=forms.PasswordInput())
   ```

2. Add the `login` view in `users/views.py`:

   ```python
   from django.contrib.auth import authenticate, login, logout
   ...

   from users.forms import UserLogin, UserRegister

   ...

   def login_user(request):
       form = UserLogin()
       if request.method == "POST":
           form = UserLogin(request.POST)
           if form.is_valid():
               auth_user = authenticate(
                 username=form.cleaned_data["username"],
                 password=form.cleaned_data["password"],
               )
               if auth_user is not None:
                   login(request, auth_user)
                   return redirect("home")

       context = {
           "form": form,
       }
       return render(request, "login.html", context)
   ```

   - Explain that the `authenticate` helper from `Django` checks the credentials and then `login` actually performs that `login session`

3. Add the `login` view to `urls.py`:

   ```python
   ...

   urlpatterns = [
       ...
       path("login/", user_views.login_user, name="login"),
   ]
   ```

4. Add the `login` template in `users/templates/login.html`:

   ```html
   <!DOCTYPE html>
   {% load crispy_forms_tags %}
   <html lang="en">
     <head>
       <meta charset="UTF-8" />
       <meta http-equiv="X-UA-Compatible" content="IE=edge" />
       <meta name="viewport" content="width=device-width, initial-scale=1.0" />
       <title>Login</title>
       <link
         rel="stylesheet"
         href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css"
         integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn"
         crossorigin="anonymous"
       />
     </head>
     <body>
       <nav class="navbar navbar-expand-lg navbar-light bg-light">
         <a class="navbar-brand" href="{% url 'home' %}">Bookstore</a>
         <button
           class="navbar-toggler"
           type="button"
           data-toggle="collapse"
           data-target="#navbarSupportedContent"
           aria-controls="navbarSupportedContent"
           aria-expanded="false"
           aria-label="Toggle navigation"
         >
           <span class="navbar-toggler-icon"></span>
         </button>

         <div class="collapse navbar-collapse" id="navbarSupportedContent">
           <ul class="navbar-nav mr-auto">
             <li class="nav-item active">
               <a class="nav-link" href="{% url 'home' %}">
                 Home <span class="sr-only">(current)</span>
               </a>
             </li>
             {% if not user.is_authenticated %}
             <li class="nav-item">
               <a class="nav-link" href="{% url 'register' %}">Sign Up</a>
             </li>
             <li class="nav-item">
               <a class="nav-link" href="{% url 'login' %}">Sign In</a>
             </li>
             {% else %}
             <li>
               <a class="nav-link" href="{% url 'logout' %}">Log Out</a>
             </li>
             {% endif %}
           </ul>
         </div>
       </nav>

       <div class="container">
         <h1>Sign In</h1>
         <form action="{% url 'login' %}" method="post">
           <!-- prettier-ignore -->
           {% csrf_token %}
           {{ form | crispy }}
           <button class="btn btn-success" type="submit">Login</button>
         </form>
       </div>
     </body>
   </html>
   ```

5. Update `home.html` and `register.html` to include the link to `login`:

   ```html
   <a class="nav-link" href="{% url 'login' %}">Sign In</a>
   ```

6. Try out the `login` form.

### Permissions

We have already seen how `permissions` work in the templates, time to get `permissions` work on the `view` level

1. Go to `http://localhost:8000/books`, and tell the students that we would like to hide this from anonymous users (i.e., unauthenticated users).
2. Go `books/views.py` and add the following at the top of `get_books`:

   ```python
   if not request.user.is_authenticated:
       raise Http404
   ```

   - This way the page does not exist for anonymous users.

3. Explain that this is a higher level of protection, and that this completely blocks the page for anonymous users, while making these checks in the template is not the same. For example, adding an `if-statement` to whether or not a link should be displayed to the user only hides it. If there is no protection on the view level, the user could still go to that page by manipulating the url in the browser.
