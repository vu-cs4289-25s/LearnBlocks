mock_user={
    "user_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
    "email": "johndoe@example.com",
    "role": "student",
    "created_at":"2025-02-11 03:14:07",
    "weekly_activity":3,
}

mock_session={
    "user_id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
}

mock_badge = {
    "badge_id": 1,
    "badge_description": "python",
    "badge_name": "Python Novice",
    "s3_url":"1.example.com",
    #a join of user, badge, relationship
    "earned_date": "2025-02-11 03:14:07"  # ISO 8601 date format
}
mock_badge2 = {
    "badge_id": 2,
    "badge_description": "block",
    "badge_name": "Block Novice",
    "s3_url":"2.example.com",
    "earned_date": "2025-02-11 03:14:07"  # ISO 8601 date format
}

mock_badge_list={
    "badges":[mock_badge,mock_badge2]
}

mock_activity={
    "student_id":1,
    "weekday":"monday",
    "date":"2025-02-11 03:14:07",
    "name":True,
}
mock_activity2={
    "student_id":1,
    "weekday":"sunday",
    "date":"2025-02-11 03:14:07",
    "name":False,
}
mock_activity_list={
    "activities":[mock_activity,mock_activity2]
}

mock_class={
    "class_id": 1,
    "class_name": "class 1",
    "class_code": "1000",
    "is_active": True,
    "created_at":"2025-02-11 03:14:07",
    #a join of user, class, relationship
    "role": "student",
    "enrollment_date":"2025-02-12 03:14:07",
}

mock_class2={
    "class_id": 2,
    "class_name": "class 2",
    "class_code": "1001",
    "is_active": True,
    "created_at":"2025-02-11 03:14:07",

    "role": "student",
    "enrollment_date":"2025-02-12 03:14:07",    
}

mock_class_list={
    "classes": [mock_class,mock_class2]
}

mock_rooster={ #currently unused
    "user_id": 1,
    "class_id": 1,
    "role": "student",
    "enrollment_date": "2025-02-11 03:14:07",
}

mock_course = {
    "course_id": 1,
<<<<<<< HEAD
    "course_name": "Introduction to Block",
    "course_description": "A beginner-friendly course introducing fundamental concepts in programming, algorithms, and data structures.",
    "status": "active",
=======
    "course_name": "Introduction to Computer Science",
    "course_description": "A beginner-friendly course introducing fundamental concepts in programming, algorithms, and data structures.",
    "course_status": "active",
>>>>>>> sqltemp
    "badge_id": 1,
    "owner_id": 2,
}

mock_course2 = {
    "course_id": 2,
<<<<<<< HEAD
    "course_name": "Introduction to Python",
    "course_description": "An introductory course covering limits, derivatives, integrals, and their applications.",
    "status": "active",
=======
    "course_name": "Calculus I",
    "course_description": "An introductory course covering limits, derivatives, integrals, and their applications.",
    "course_status": "active",
>>>>>>> sqltemp
    "badge_id": 2,
    "owner_id": 2,
}

<<<<<<< HEAD
=======
# Optionally, store the courses in a list for easy access
>>>>>>> sqltemp
courses = [mock_course, mock_course2]
mock_course_list={
    "courses": courses
}

module_data_1 = {
    "module_id": 1,        # integer module id
    "module_name": "Introduction to Python",
    "status": "active",
    "owner_id": 2,

    #join course, module
    "course_id": 1,      # assuming course_id is represented as an integer
    "module_order": 1,     # integer order indicating the module's position
}

module_data_2 = {
    "module_id": 2,
    "module_name": "Advanced Python Techniques",
    "status": "active",
    "owner_id": 2,

    "course_id": 1,
    "module_order": 2,
}

# Group the modules in a list for easy access or iteration
modules = [module_data_1, module_data_2]

module_list={
    "modules":modules
}


progress_data_1={
    "progress_id":1,
    "student_id":1,
    "module_id":1,
    "status":"completed",
    "completion_date":"2025-02-11 03:14:07",
}
progress_data_2={
    "progress_id":2,
    "student_id":1,
    "module_id":2,
    "status":"active",
    "completion_date":"2025-02-12 03:14:07",
}
progresses=[progress_data_1,progress_data_2]

progress_list={
    "progresses":progresses
}

assignment_data_1={
    "assignment_id":5,
    "class_id":1,
    "module_id":1,
    "assigned_date":"2025-02-12 03:14:07",
    "due_date": "2025-02-20 03:14:07"
}
assignment_data_2={
    "assignment_id":6,
    "class_id":1,
    "module_id":2,
    "assigned_date":"2025-02-13 03:14:07",
    "due_date": "2025-02-20 03:14:07",
}

assignments=[assignment_data_1,assignment_data_2]

assignment_list={
    "assignments":assignments
}

project_data_1={
    "project_id":1,
    "user_id": 1,
    "project_name": "New project",
    "module_id": 1,
    "s3_url": "project1.example.com",
    "created_at": "2025-02-12 03:14:07",
    "last_modified": "2025-02-13 03:14:07",
}

projects=[project_data_1]