# Survey App

This is a Django app that makes surveys. With it, users can create their own surveys and answer them. Choices are saved so that people can see how many votes each choice has.

## Getting Started

This app was written with Django 3.1.2. 

First, you will need to create a **private_settings.py** file in the survey2 directory. In it, you will need to store private settings (ie. SECRET_KEY). 

Second, it's recommended to use python's **virtualenv** tool if building locally:

> $ mkvirtualenv *django_env*
> $ python manage.py runserver

Then visit http://localhost:8000 in your web browser to view the app. 

Third, to access the survey functions of the site, a login is required. You can create a superuser from the terminal to explore the site.

> python manage.py createsuperuser

Follow the prompts to create your username, email, and password to login to the site.

## Screenshots

![ss1](/screenshots/1.png?raw=true)
![ss3](/screenshots/3.png?raw=true)
![ss4](/screenshots/4.png?raw=true)
![ss5](/screenshots/5.png?raw=true)