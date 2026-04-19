#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput --clear --ignore=cloudinary
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin69').exists():
    User.objects.create_superuser('admin69', 'admin@ecrochet.com', 'Admin@1234')
    print('Superuser created!')
else:
    print('Superuser already exists.')
"