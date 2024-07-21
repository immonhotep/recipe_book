#recipe_book

A simple recipe book application written in python-django, and used free modified bootsrap templates - elements in frontend.
Application pure django not contain javascripts - update, and delete functions made with modals.

Reason of the application: Learn - Practise django, and python

Application functions:
- User registration, and login
- manage accounts
- upload, modify, and delete recipes
- upload, modify, and delete categories ( superuser only)
- create, modify, and delete comments
- like or unlike recipes, and comments
-  deactivate or reactivate user account (superuser only)


Installation:

1. clone this  repo: git clone https://github.com/immonhotep/recipe_book.git
2. cd recipe_book
3. create virtual environment and activate it: ( virtualenv .venv  && source .venv/bin/activate
4. install requirements:    pip3 install -r requirements
5. perform database changes: python3 manage.py migrate
6. create admin user:  python3 manage.py createsuperuser
7. start using application:  python3 manage.py runserver
8. optional: when first category, or first user profile created - media directory automatically will also created. To use default images need 2 image files to the following path and name:
   
media/images/default.jpg

media/images/default_user.jpg  

( on internet can find files for this easy ), but without these images application should work fluently.
