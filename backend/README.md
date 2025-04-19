Updated at 03/24
# Start Backend
python manage.py runserver at root directory of project.
# DB Connection
Change the sample db info in the backend/settings.py DATABASES['default'] to the actual db info.

# Known Issues
Table with composite primary key(the rooster table) have issue defining many-to-many relationship. Django seems to not support composite primary key, will try to solve it.
