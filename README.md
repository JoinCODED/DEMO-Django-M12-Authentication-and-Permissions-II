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


   def registration(request):
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
       path("register/", user_views.registration, name="register"),
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
