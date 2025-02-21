mock_user={
    "user_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "username": "johndoe",
    "email": "johndoe@example.com",
    "city": "New York",
    "state": "NY",
    "role": "student"
}

mock_session={
    "user_id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
}

mock_badge = {
    "badge_id": 1,
    "student_id": 1,
    "badge_name": "Python Novice",
    "earned_date": "2025-02-11"  # ISO 8601 date format
}

mock_badge2 = {
    "badge_id": 2,
    "student_id": 1,
    "badge_name": "Block Novice",
    "earned_date": "2025-02-11"  # ISO 8601 date format
}

mock_badge_list={
    "badges":[mock_badge,mock_badge2]
}

mock_activity={
    "student_id":1,
    "weekday":"monday",
    "date":"2025-02-11",
    "name":True,
}
mock_activity2={
    "student_id":1,
    "weekday":"sunday",
    "date":"2025-02-11",
    "name":False,
}
mock_activity_list={
    "activities":[mock_activity,mock_activity2]
}

mock_class={
    "class_id": 1,
    "class_name": "python class",
    "teacher_id": 2,
    "created_at":"2025-02-11",
}

mock_class2={
    "class_id": 2,
    "class_name": "block class",
    "teacher_id": 2,
    "created_at":"2025-02-11",
}

mock_class_list={
    "classes": [mock_class,mock_class2]
}

mock_rooster={
    "user_id": 1,
    "class_id": 1,
    "role": "student",
    "enrollment_date": "2025-02-11",
}

mock_course = {
    "course_id": 1,
    "course_name": "Introduction to Computer Science",
    "course_description": "A beginner-friendly course introducing fundamental concepts in programming, algorithms, and data structures."
}

mock_course2 = {
    "course_id": 2,
    "course_name": "Calculus I",
    "course_description": "An introductory course covering limits, derivatives, integrals, and their applications."
}

# Optionally, store the courses in a list for easy access
courses = [mock_course, mock_course2]
mock_course_list={
    "courses": courses
}

module_data_1 = {
    "module_id": 1,        # integer module id
    "course_id": 1,      # assuming course_id is represented as an integer
    "module_name": "Introduction to Python",
    "module_order": 1,     # integer order indicating the module's position
    "module_status": "active"
}

module_data_2 = {
    "module_id": 2,
    "course_id": 1,
    "module_name": "Advanced Python Techniques",
    "module_order": 2,
    "module_status": "active"
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
    "completion_date":"2025-02-11",
}
progress_data_2={
    "progress_id":2,
    "student_id":1,
    "module_id":2,
    "status":"active",
    "completion_date":"2025-02-12",
}
progresses=[progress_data_1,progress_data_2]

progress_list={
    "progresses":progresses
}

assignment_data_1={
    "course_assignment_id":5,
    "class_id":1,
    "course_id":1,
    "assigned_date":"2025-02-12",
}
assignment_data_2={
    "course_assignment_id":6,
    "class_id":1,
    "course_id":2,
    "assigned_date":"2025-02-13",
}

assignments=[assignment_data_1,assignment_data_2]

assignment_list={
    "assignments":assignments
}

