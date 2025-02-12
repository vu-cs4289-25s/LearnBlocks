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