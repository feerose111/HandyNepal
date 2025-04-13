#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input

if [[ $CREATE_SUPERUSER ]];
then
  python manage.py createsuperuser --no-input --email "$DJANGO_SUPERUSER_EMAIL"
fi

& "C:\Program Files\PostgreSQL\17\bin\psql.exe" "postgresql://handynepal_django_user:W46DZeezU5JsKX0I6tixlUII90oBSRNv@dpg-cvt6kahr0fns73e1it0g-a.singapore-postgres.render.com/handynepal_django" < local_backup.sql

chmod +x build.sh