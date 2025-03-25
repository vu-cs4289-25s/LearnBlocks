Updated at 03/24
# Start Backend
python manage.py runserver at root directory of project.
# DB Connection
Change the sample db info in the backend/settings.py DATABASES['default'] to the actual db info.

# API endpoint
The endpoint is defined in backend/urls.py urlpatterns. For single-table CRUD, it is defind like:
(suppose PATH is http://127.0.0.1:8000/api/)
GET all items in table
GET PATH/table/

GET items in table of specific id
GET PATH/{:id}

POST items in table
POST PATH/table/
the field name of the request body is defined at 
learnblocks/models.py

Note that all fields in model need to be in post request body, **EXCEPT**:
a. Field marked as AutoField, it is typically id field. If not provided, will auto generated.
b. Field marked as DateField or DateTimeField. If not provided, will generate by current time.
c. Field marked as (null=true)

example:
/projects/
{
"project_name": "Finaect",
"s3_url": "https://s3.amazonaws.com/projects/final_python_project.zip",
"user": 1,
"module": 2
}

(TODO: S3 machanisms will implement in the future, this is just of a demo of POST)

PUT PATH/table/{:id}
Similar to POST, but could only provide fields needs to be updated.

DELETE PATH/table/{:id}

# Known Issues
Table with composite primary key(the rooster table) have issue defining many-to-many relationship. Django seems to not support composite primary key, will try to solve it.
