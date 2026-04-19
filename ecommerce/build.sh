#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from app.models import Category
cats = ['Accessories', 'Clothings', 'Bags', 'Decor Items']
for c in cats:
    Category.objects.get_or_create(name=c)
print('Categories created!')
"

python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ecrochet.com', 'Admin@1234')
    print('Superuser created!')
else:
    print('Superuser already exists.')
"