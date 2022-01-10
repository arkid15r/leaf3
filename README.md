1. `git clone https://github.com/arkid15r/django-project-boilerplate.git`
2. `mv django-project-boilerplate project_name; cd project_name`
3. `virtualenv venv; source venv/bin/activate`
4. `pip install -r requirements/local.txt`
5. `python manage.py migrate`
6. Run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` and place the output into config/.env SECRET_KEY
7. `python manage.py runserver`
