/* ======================== AUTHENTICATION & USER MANAGEMENT ======================== */

/* Get user by email (used for login) */
SELECT * FROM "user" WHERE email = :email;

/* Select first name */
SELECT first_name FROM "user" WHERE user_id = :userId;

/* Check user role */
SELECT role FROM "user" WHERE user_id = :userId;

/* Get public user profile */
SELECT * FROM "user" WHERE username = :username;

/* Get private user profile */
SELECT * FROM "user" WHERE user_id = :userId;

/* Check weekly activity */
SELECT weekly_activity FROM "user" WHERE user_id = :userId;

/* Create a new user */
INSERT INTO "user" (role, first_name, last_name, username, email, password_hash)
VALUES (:role, :first_name, :last_name, :username, :email, :password_hash);

/* Update user details */
UPDATE "user" 
SET first_name = :newFirstName, last_name = :newLastName, email = :newEmail
WHERE user_id = :userId;

/* Update user role */
UPDATE "user" SET role = :newRole WHERE user_id = :userId;

/* Delete a user */
DELETE FROM "user" WHERE user_id = :userId;

/* ======================== CLASS MANAGEMENT ======================== */

/* Get all active classes */
SELECT * FROM "class" WHERE is_active = TRUE;

/* Get a specific class */
SELECT * FROM "class" WHERE class_id = :classId;

/* Get a class by its class code */
SELECT * FROM "class" WHERE class_code = :classCode;

/* Get all classes owned by a teacher */
SELECT * FROM "class" 
WHERE class_id IN (
    SELECT class_id FROM "user_class_roster" WHERE user_id = :teacherId AND role = 'owner'
);

/* Create a new class with auto-generated class code */
INSERT INTO "class" (class_name, class_code, is_active, created_at)
VALUES (:className, LEFT(MD5(random()::text), 8), TRUE, CURRENT_TIMESTAMP)
RETURNING class_id, class_code;

/* Update class name */
UPDATE "class" SET class_name = :newClassName WHERE class_id = :classId;

/* Archive a class */
UPDATE "class" SET is_active = FALSE WHERE class_id = :classId;

/* Reactivate an archived class */
UPDATE "class" SET is_active = TRUE WHERE class_id = :classId;

/* Delete a class */
DELETE FROM "class" WHERE class_id = :classId;

/* ======================== COURSE MANAGEMENT ======================== */

/* Get all public courses */
SELECT * FROM "course" WHERE permission = 'public';

/* Get all courses owned by a teacher */
SELECT * FROM "course" WHERE owner_id = :teacherId;

/* Get all courses a student is enrolled in */
SELECT c.* FROM "course" c
JOIN "user_course_enrollment" uce ON c.course_id = uce.course_id
WHERE uce.user_id = :userId;

/* Get a specific course */
SELECT * FROM "course" WHERE course_id = :courseId;

/* Update course visibility */
UPDATE "course" SET permission = :newPermission WHERE course_id = :courseId AND owner_id = :teacherId;

/* ======================== MODULE MANAGEMENT ======================== */

/* Get all modules in a specific course */
SELECT * FROM "module" 
WHERE module_id IN (SELECT module_id FROM module_course_mapping WHERE course_id = :courseId);

/* Get module by ID */
SELECT * FROM "module" WHERE module_id = :moduleId;

/* Create a new module */
INSERT INTO "module" (module_name, status, owner_id)
VALUES (:moduleName, :status, :ownerId);

/* Update module name */
UPDATE "module" SET module_name = :newModuleName WHERE module_id = :moduleId;

/* Update module status */
UPDATE "module" SET status = :newStatus WHERE module_id = :moduleId;

/* ======================== BADGES & ACHIEVEMENTS ======================== */

/* Get all badges */
SELECT * FROM "badge";

/* Get a specific badge */
SELECT * FROM "badge" WHERE badge_id = :badgeId;

/* Get all badges earned by a user */
SELECT b.* FROM "badge" b
JOIN "user_badge_achievement" uba ON b.badge_id = uba.badge_id
WHERE uba.user_id = :userId;

/* Award a badge to a user */
INSERT INTO "user_badge_achievement" (badge_id, user_id, earned_date)
VALUES (:badgeId, :userId, CURRENT_TIMESTAMP);

/* ======================== PROJECT SUBMISSIONS ======================== */

/* Get all projects for a user */
SELECT * FROM "project" WHERE user_id = :userId;

/* Get a project by ID */
SELECT * FROM "project" WHERE project_id = :projectId;

/* Create a new project */
INSERT INTO "project" (user_id, project_name, module_id, s3_url)
VALUES (:userId, :projectName, :moduleId, :s3Url);

/* Update a project */
UPDATE "project" 
SET project_name = :newProjectName, last_modified = CURRENT_TIMESTAMP 
WHERE project_id = :projectId;

/* Delete a project */
DELETE FROM "project" WHERE project_id = :projectId;

/* ======================== CLASS ENROLLMENT ======================== */

/* Get all classes a student is enrolled in */
SELECT c.* FROM "class" c
JOIN "user_class_roster" ucr ON c.class_id = ucr.class_id
WHERE ucr.user_id = :userId;

/* Add a student to a class */
INSERT INTO "user_class_roster" (user_id, class_id, role, enrollment_date)
VALUES (:userId, :classId, 'participant', CURRENT_DATE);

/* Remove a student from a class */
DELETE FROM "user_class_roster" WHERE user_id = :userId AND class_id = :classId;

/* ======================== COURSE ENROLLMENT ======================== */

/* Enroll a student in a course */
INSERT INTO "user_course_enrollment" (course_id, user_id, role)
VALUES (:courseId, :userId, 'participant');

/* Unenroll a student from a course */
DELETE FROM "user_course_enrollment" WHERE user_id = :userId AND course_id = :courseId;

/* ======================== MODULE PROGRESS TRACKING ======================== */

/* Get module progress for a user */
SELECT * FROM "user_module_progress" WHERE user_id = :userId;

/* Update module progress */
UPDATE "user_module_progress" 
SET status = :newStatus 
WHERE user_id = :userId AND module_id = :moduleId;

/* ======================== CLASS ASSIGNMENTS ======================== */

/* Get assignments for a class */
SELECT * FROM "class_module_assignment" WHERE class_id = :classId;

/* Create a new assignment */
INSERT INTO "class_module_assignment" (class_id, module_id, assigned_date, due_date)
VALUES (:classId, :moduleId, CURRENT_TIMESTAMP, :dueDate);

/* ======================== COURSE-CLASS MAPPING ======================== */

/* Get courses assigned to a class */
SELECT c.* FROM "course" c
JOIN "course_class_mapping" ccm ON c.course_id = ccm.course_id
WHERE ccm.class_id = :classId;

/* Assign a course to a class */
INSERT INTO "course_class_mapping" (course_id, class_id, assigned_date)
VALUES (:courseId, :classId, CURRENT_TIMESTAMP);

/* ======================== MODULE-COURSE MAPPING ======================== */

/* Get modules in a course */
SELECT m.* FROM "module" m
JOIN "module_course_mapping" mcm ON m.module_id = mcm.module_id
WHERE mcm.course_id = :courseId
ORDER BY mcm.module_order;

/* Add a module to a course */
INSERT INTO "module_course_mapping" (course_id, module_id, module_order)
VALUES (:courseId, :moduleId, :moduleOrder);