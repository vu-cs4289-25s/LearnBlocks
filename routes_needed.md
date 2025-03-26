should be served on api.learnblocks.com
frontend will be learnblocks.com
all requests should use the learnblocks cookie for authorization
think through permissions, who can do what
for example, we adding POSTing badges can be admin only authenticated users. All other users do not have authorization

# AUTH

## POST "/login"
- request:
	-	body: 
		- username
		- password
- response:
	-	set learnblocks cookie
		
## GET "/whoami" 
- request:
	- cookie:
		- learnblocks
- response:
	- user 

## DELETE "/logout"
- request:
	- cookie:
		- learnblocks
- response:
	- set learnblocks cookie

# USER 

## POST "/users"
- request:
	- body:
		- data
response:
	- body:
		- user

## GET "/users/{userid}"
- request:
	- params:
		- userid
response:
	- body:
		- user

## PATCH "/users/{userid}"
- request:
	- params:
		- userid
	- body:
		- data
response:
	- body:
		- user

## DELETE "/users/{userid}"
- request:
	- params:
		- userid
response:
	- body:
		- user


# PROJECTS

## POST "/projects"
- request:
	- body:
		- project_data
response:
	- body:
		- project

## GET "/projects/{projectid}"
- request:
	- params:
		- projectid
response:
	- body:
		- project

## PATCH "/projects/{projectid}"
- request:
	- params:
		- projectid
	- body:
		- data
response:
	- body:
		- project

## DELETE "/projects/{projectid}"
- request:
	- params:
		- projectid
response:
	- body:
		- project

## GET "/projects/user/{userid}"
- request:
	- params:
		- userid
response:
	- body:
		- projects

## GET "/projects/{projectid}/blob"
- request:
	- params:
		- projectid
response:
	- body:
		- project_blob


# BADGE

## POST "/badges"
- request:
	- body:
		- badge_data
response:
	- body:
		- badge

## GET "/badges/{badgeid}"
- request:
	- params:
		- badgeid
response:
	- body:
		- badge

## PATCH "/badges/{badgeid}"
- request:
	- params:
		- badgeid
	- body:
		- data
response:
	- body:
		- badge

## DELETE "/badges/{badgeid}"
- request:
	- params:
		- badgeid
response:
	- body:
		- badge

## GET "/badges/user/{userid}"
- request:
	- params:
		- userid
response:
	- body:
		- badges

## GET "/badges/{badgeid}/image"
- request:
	- params:
		- badgeid
response:
	- body:
		- badge_image


# COURSE

## POST "/courses"
- request:
	- body:
		- course_data
response:
	- body:
		- course

## GET "/courses/{courseid}"
- request:
	- params:
		- courseid
response:
	- body:
		- course

## PATCH "/courses/{courseid}"
- request:
	- params:
		- courseid
	- body:
		- data
response:
	- body:
		- course

## DELETE "/courses/{courseid}"
- request:
	- params:
		- courseid
response:
	- body:
		- course

## GET "/courses/user/{ownerid}"
- request:
	- params:
		- ownerid
response:
	- body:
		- courses

## GET "/courses/class/{classid}"
- request:
	- params:
		- classid
response:
	- body:
		- courses


# MODULES

## POST "/modules"
- request:
	- body:
		- module_data
response:
	- body:
		- module

## GET "/modules/user/{ownerid}"
- request:
	- params:
		- ownerid
response:
	- body:
		- modules

## GET "/modules/{moduleid}/user_progress/{userid}"
- request:
	- params:
		- userid
response:
	- body:
		- module_progress


## GET "/modules/course/{courseid}"
- request:
	- params:
		- courseid
response:
	- body:
		- modules

## GET "/modules/{moduleid}"
- request:
	- params:
		- moduleid
response:
	- body:
		- module

## GET "/modules/{moduleid}/intructions"
- request:
	- params:
		- moduleid
response:
	- body:
		- module_instructions_blob

## PATCH "/modules/{moduleid}"
- request:
	- params:
		- moduleid
	- body:
		- data
response:
	- body:
		- module

## DELETE "/modules/{moduleid}"
- request:
	- params:
		- moduleid
response:
	- body:
		- module


# CLASS

## POST "/classes"
- request:
	- body:
		- class_data
response:
	- body:
		- class

## GET "/classes/user/{ownerid}"
- request:
	- params:
		- ownerid
response:
	- body:
		- classes

## GET "/classes/enrollment/user/{userid}"
- request:
	- params:
		- userid
response:
	- body:
		- classes

## GET "/classes/{classid}"
- request:
	- params:
		- classid
response:
	- body:
		- class

## PATCH "/classes/{classid}"
- request:
	- params:
		- classid
	- body:
		- data
response:
	- body:
		- class

## DELETE "/classes/{classid}"
- request:
	- params:
		- classid
response:
	- body:
		- class


