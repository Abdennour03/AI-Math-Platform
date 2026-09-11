# EduInsight AI Architecture

## Current Architecture

The backend is a layered FastAPI application:

```text
HTTP request
  -> api/routes and Pydantic schemas
  -> controllers
  -> services
  -> repositories
  -> database.Database / sqlite3
  -> eduinsight.db
```

The dependency direction is one-way. Routes do not import repositories, and controllers do not import repositories. The application composition root is `api/dependencies.py`:

```text
Database
  -> repositories
  -> services
  -> controllers
  -> routes
```

`app.py` exports `api.main.app`, so the application can be started with `uvicorn app:app`.

## Responsibilities

- `api/`: HTTP routes, request/response schemas, authentication dependencies, and serialization.
- `controllers/`: thin use-case facades. Controllers delegate to one service and contain no persistence logic.
- `services/`: business rules, validation orchestration, authorization decisions, password hashing, JWT creation, relationship checks, and workflows.
- `repositories/`: SQL queries, inserts, updates, deletes, and model hydration only. They do not raise HTTP exceptions or depend on FastAPI.
- `models/`: plain domain entities.
- `database/database.py`: the single SQLite connection and schema owner. It enables foreign keys and creates all tables without deleting existing data.
- `utils/`: reusable validation and security helpers.
- `tests/`: repository, service, and controller tests.

## Request Lifecycle

A route validates transport data with Pydantic, obtains the authenticated user where required, calls a controller, and serializes the returned model. The controller delegates to a service. The service validates business rules and calls repositories. A repository performs SQL through the shared `Database` connection and returns a model or persistence result.

HTTP concerns remain in routes. For example, grade ownership and duplicate prevention are not implemented in `grade_router.py`; they are enforced by `GradeService` before `GradeRepo` persists the grade.

## Business Rules

`GradeService` enforces:

- scores are validated by `utils/validators.py` against `Exercise.max_score`;
- students and exercises must exist;
- a student can have at most one grade for an exercise;
- a teacher can create, update, or delete grades only for exercises owned by
  that teacher;
- teachers can manage only their own courses and exercises.

The SQLite `UNIQUE(student_id, exercise_id)` constraint is a persistence backstop. The service performs the business decision and returns a meaningful conflict error. `Exercise.max_score` is stored in the `exercises` table. Existing databases receive this column through a non-destructive migration in `database/database.py`, defaulting to `20`.

Authentication follows `Auth route -> AuthController -> AuthService -> student/teacher repositories -> SQLite`. JWT helpers remain in `utils/security.py`. Current-user dependencies resolve users through services, preserving student and teacher role checks.

Admin authentication follows the same flow with `AdminRepo` as an additional
credential source. Successful admin logins receive a JWT with
`role: "admin"`. The `get_current_admin` dependency resolves and authorizes
admin users; every protected `/admin/*` route depends on it.

Classes are represented by the `ClassGroup` domain model and persisted in the
`classes` table. Students keep one optional `class_id`. Teachers use the
`teacher_classes` junction table, so one teacher may teach multiple classes
and one class may have multiple teachers. Existing scalar teacher assignments
are migrated into the junction table.

Admin business operations include:

- creating and updating the authenticated admin profile;
- creating an admin through the public `POST /admin/setup` bootstrap route;
- creating, searching, updating, and deleting students and teachers;
- creating, updating, listing, and deleting classes;
- assigning students to one class;
- replacing a teacher's assigned class set through
  `POST /admin/teachers/{teacher_id}/classes`;
- returning a complete student academic report with class information,
  exercises, and nullable scores.

Attendance operations include:

- allowing a teacher to retrieve the students in one of their assigned classes;
- saving one attendance status per student, class, and date;
- updating an existing attendance record for the same student and date;
- allowing teachers to view attendance history for their assigned classes;
- allowing administrators to retrieve a monthly attendance report by class.

Attendance statuses are restricted to `present` and `absent`. The attendance
service verifies that the selected class belongs to the teacher and that every
submitted student belongs to that class before any record is written.

## Persistence Reality

This project uses raw `sqlite3`; it does not use SQLAlchemy or another ORM.
Schema creation is centralized in `Database.create_tables()` and is
idempotent. It creates the Admin, Class, and teacher-class relationship tables,
adds non-destructive compatibility columns where required, migrates legacy
teacher class assignments, and seeds the initial admin account when it is not
present:

```text
email:    admin@eduinsight.ai
password: adminpassword
```

Attendance is stored in the `attendance` table:

```text
attendance_id | student_id | class_id | date       | status
-----------------------------------------------------------
1             | 1          | 1         | 2026-09-11 | present
2             | 2          | 1         | 2026-09-11 | absent
```

The table has a unique constraint on `(student_id, class_id, date)`. Saving
attendance uses SQLite upsert behavior, so correcting a student's status for
the same day updates the existing row instead of creating a duplicate.

The SQLite database file may be deleted for a clean local reset; restarting
the application recreates the schema and seed admin. No ORM migration was
introduced.

## Structure

```text
app.py
api/
  main.py
  dependencies.py
  routes/
  schemas/
  routes/admin_router.py
  schemas/admin_schemas.py
controllers/
  admin_controller.py
  attendance_controller.py
  class_controller.py
services/
  admin_service.py
  attendance_service.py
  class_service.py
repositories/
  admin_repository.py
  attendance_repository.py
  class_repository.py
models/
  attendance.py
database/database.py
utils/
tests/
  controllers/
  services/
  repositories/
data/
config/
```

## Refactor Record

Before the refactor, `api/dependencies.py` passed repositories directly to several controllers, some constructors had invalid argument counts, notification business logic lived in `NotificationController`, student notifications bypassed controllers, and `all_code.py`, `reste.py`, and the CLI views duplicated stale implementations. Repository constructors also created tables independently.

After the refactor:

- dependency construction is Database -> Repository -> Service -> Controller;
- Admin and Class entities were added through the same dependency direction;
- admin authentication and protected administrative routes were added;
- public admin bootstrap was added at `POST /admin/setup`;
- teacher-to-class changed from a scalar foreign key to the `teacher_classes`
  many-to-many junction table;
- notification and authentication workflows moved from controllers into services;
- grade teacher ownership moved from routes into `GradeService`;
- attendance management was added through `AttendanceRepo`,
  `AttendanceService`, `AttendanceController`, and attendance routes;
- attendance records use a unique student/class/date key and upsert on correction;
- student-notification routes use `NotificationController` and `NotificationService`;
- schema creation moved into `database/database.py`;
- `CourseController` was implemented as a service facade;
- stale CLI/view and monolithic copies were removed;
- tests moved from the non-executable `test/` scripts to `tests/controllers`, `tests/services`, and `tests/repositories`.

Removed files were obsolete `all_code.py`, `reste.py`, the old CLI view
modules, and the old import-time test scripts. The SQLite database is treated
as local runtime state and is recreated by the database gateway when absent.

## Verification

The following checks were performed:

- compiled all API, controller, service, repository, model, utility, and database modules;
- imported the complete FastAPI application successfully;
- exercised grade creation, duplicate rejection, ownership rejection, and authorized update against a temporary SQLite database;
- exercised admin setup, admin JWT role resolution, class creation, and
  teacher assignment to multiple classes against temporary SQLite databases;
- exercised attendance saving, same-day correction, teacher class ownership,
  student membership validation, and monthly history against temporary SQLite
  databases;
- verified legacy class/admin migration and the OpenAPI Admin and teacher
  response contracts;
- added pytest coverage for the database schema, controller delegation, and grade business rules.

Run the full suite with:

```bash
python -m pytest -q
```

## Software Engineering Design Patterns

### 1. Layered Architecture

The project uses **Layered Architecture** to separate technical concerns:

```text
Presentation      api/routes, api/schemas
Application       controllers
Business          services
Persistence       repositories
Infrastructure    database/database.py and SQLite
```

Each layer may depend on the layer below it, but lower layers must not depend
on HTTP routes or FastAPI. This makes business rules testable without starting
the web server.

### 2. Service Layer Pattern

Services are the application boundary for use cases and business rules.
Examples include:

- `GradeService.create_grade`: validates the score against
  `Exercise.max_score`, verifies related entities, checks teacher ownership,
  and prevents duplicate grades.
- `AuthService.login`: finds a user, verifies the password, and creates a JWT.
- `NotificationService`: creates notifications and coordinates delivery to
  one or many students.

Controllers do not decide these rules. They delegate to services and keep the
HTTP-facing API stable.

### 3. Repository Pattern

Repositories encapsulate SQLite operations and model hydration. A service
asks a repository for domain data rather than knowing SQL details.

Repositories may query, insert, update, delete, and count records. They must
not perform authorization, hash passwords, raise `HTTPException`, or depend on
FastAPI.

### 4. Dependency Injection and Composition Root

`api/dependencies.py` is the **Composition Root**. It constructs the object
graph once in dependency order:

```text
Database
  -> StudentRepo, TeacherRepo, CourseRepo, ...
  -> StudentService, TeacherService, CourseService, ...
  -> StudentController, TeacherController, CourseController, ...
  -> API routes
```

Classes receive their collaborators through constructors. This is constructor
injection and allows tests to provide temporary databases, fake repositories,
or test doubles without changing business code.

### 5. Facade Pattern

Controllers act as thin **facades** over services. For example,
`GradeController` exposes operations used by routes while the details remain
inside `GradeService`. This provides a stable boundary between HTTP handlers
and application use cases.

### 6. Data Transfer Object Pattern

Pydantic schemas in `api/schemas/` are transport DTOs. They define the shape
of incoming and outgoing HTTP data and prevent API payloads from becoming
domain objects. Repositories and services work with models such as
`Student`, `Course`, and `Grade`.

### 7. Domain Model Pattern

Files in `models/` contain plain entities. They represent state and
relationships without FastAPI, SQL queries, or response serialization. This
keeps domain data independent from the delivery mechanism.

### 8. Policy and Validation Pattern

Reusable validators in `utils/` centralize field-level rules such as valid
names, passwords, score ranges, maximum scores, course data, and notification
content. Services combine these validators with cross-entity rules such as
ownership and duplicate prevention.

### 9. Gateway Pattern for Persistence

The `Database` class is the infrastructure gateway for SQLite. It owns the
connection, enables foreign keys, and creates the schema. Repositories use
this gateway instead of opening independent database connections or creating
tables during construction.

## SOLID Principles Applied

| Principle | Application in EduInsight AI |
| --- | --- |
| Single Responsibility | Routes handle HTTP, services handle business rules, repositories handle SQL. |
| Open/Closed | Services can receive alternate repository implementations in tests. |
| Liskov Substitution | Repository collaborators expose the operations expected by their services. |
| Interface Segregation | Each repository is focused on one aggregate or relationship. |
| Dependency Inversion | Controllers depend on services and services depend on repository abstractions at their boundary, not on FastAPI or SQL statements. |

The project currently uses concrete Python classes rather than formal abstract
repository interfaces. Introducing `Protocol` or `ABC` contracts is a future
improvement if multiple persistence implementations are required.

## Request Sequence Example

The teacher grade workflow follows this sequence:

```text
Teacher
  -> POST /teachers/me/grades
  -> teacher_router.add_grade_to_student
  -> GradeController.create_grade
  -> GradeService.create_grade
       - validate score
       - load student and exercise
       - verify exercise ownership
       - check existing grade
  -> GradeRepo.add_grade
  -> SQLite grades table
```

The teacher attendance workflow follows this sequence:

```text
Teacher
  -> GET /teachers/me/attendance/classes/{class_id}/students
  -> AttendanceController.get_class_students
  -> AttendanceService.get_class_students
       - verify the class exists
       - verify the teacher is assigned to the class
       - load students assigned to the class

Teacher
  -> POST /teachers/me/attendance
  -> AttendanceController.save_attendance
  -> AttendanceService.save_attendance
       - validate statuses and duplicate student entries
       - verify every student belongs to the selected class
       - upsert attendance by student, class, and date
  -> AttendanceRepo.save_attendance
  -> SQLite attendance table
```

Administrators can retrieve the same stored records with:

```text
GET /admin/attendance/report?class_id=1&month=2026-09
```

The `month` query parameter uses `YYYY-MM` format.

The route does not query the database and does not decide whether the teacher
owns the exercise.

## Error Boundary Rules

- Pydantic validation errors are handled by FastAPI at the API boundary.
- Services raise domain/application errors such as `ValueError` when a use
  case cannot proceed.
- Routes translate those errors into HTTP responses.
- Repositories report persistence failures and do not construct HTTP responses.

This keeps HTTP status codes out of the business layer.

## Testing Strategy

Tests are organized by architectural layer:

```text
tests/repositories  -> schema and persistence behavior
tests/services      -> business rules and authorization
tests/controllers   -> delegation contracts
```

Service tests use temporary SQLite databases. The most important grade cases
are covered: successful creation, duplicate rejection, cross-teacher rejection,
and authorized update.

Attendance service tests cover successful saving, same-day status correction,
rejection of students from another class, and filtering teacher history by
month.

Future API tests should use FastAPI's test client to verify authentication,
status codes, response schemas, and route serialization without asserting SQL
implementation details.

## Removed Anti-Patterns

The refactor removed or corrected these patterns:

- routes calling repositories directly;
- controllers receiving repositories instead of services;
- business rules duplicated between routes, controllers, and repositories;
- repositories creating tables during object construction;
- a monolithic `all_code.py` copy of the application;
- stale CLI views and import-time test scripts;
- controllers containing notification and authentication workflows.

These changes reduce duplication and make the dependency direction visible in
the source code.

## Trade-offs and Future Improvements

The current design deliberately keeps raw SQLite because it preserves the
existing database and avoids an unsafe ORM migration. The next engineering
steps could be:

1. Add formal repository `Protocol` contracts.
2. Introduce a database session or unit-of-work abstraction for transactions.
3. Replace generic `ValueError` with typed application exceptions.
4. Add API integration tests for every route family.
5. Add migrations before changing the persistence technology.
6. Implement analytics as a separate service when its requirements are clear.
