# Combined source copy


# ===== BEGIN models/teacher.py =====
class Teacher:
    def __init__(self, teacher_id, full_name, email, password, phone_number):
            self.teacher_id = teacher_id
            self.full_name = full_name
            self.email = email
            self.password = password
            self.phone_number = phone_number
# ===== END models/teacher.py =====


# ===== BEGIN controllers/teacher_controller.py =====
from models.teacher import Teacher
from utils.teacher_validation import TeacherValidator
from utils.security import hash_password

class TeacherController:
    def __init__(self, teacher_repo):
        self.teacher_repo = teacher_repo
        
        
    def create_teacher(self, full_name, email, password, phone_number):
        validation = TeacherValidator()
        validation.validate_name(full_name)
        validation.validate_email(email)
        validation.validate_password(password)
        validation.validate_phone_number(phone_number)
        hashed_password = hash_password(password)
        teacher = Teacher(None, full_name, email, hashed_password, phone_number)
        self.teacher_repo.add_teacher(teacher)
        return teacher
        

    def get_teacher(self, teacher_id):
        if not isinstance(teacher_id, int):
            raise ValueError("Teacher Id must be an integer.")
        teacher = self.teacher_repo.get_teacher(teacher_id)
        if teacher is None:
            raise ValueError("Teacher not found.")
        return teacher


    def get_all_teachers(self):
            teachers = self.teacher_repo.get_all_teachers()
            if not teachers:
                raise ValueError("No teachers found.")
            return teachers
        
    def update_teacher(self, teacher_id, **kwargs):

        teacher = self.teacher_repo.get_teacher(teacher_id)

        if teacher is None:
            raise ValueError("Teacher not found.")

        if "full_name" in kwargs:
            TeacherValidator.validate_name(kwargs["full_name"])

        if "email" in kwargs:
            TeacherValidator.validate_email(kwargs["email"])

        if "password" in kwargs:
            TeacherValidator.validate_password(kwargs["password"])
            kwargs["password"] = hash_password(kwargs["password"])

        if "phone_number" in kwargs:
            TeacherValidator.validate_phone_number(kwargs["phone_number"])

        self.teacher_repo.update_teacher(
            teacher_id,
            **kwargs
        )

        return "Teacher updated successfully"
    
    def delete_teacher(self, teacher_id):
            if not isinstance(teacher_id, int):
                raise ValueError("teacher ID must be an integer")
            teacher = self.teacher_repo.get_teacher(teacher_id)
            if teacher is None:
                raise ValueError("teacher is not found.")
            self.teacher_repo.delete_teacher(teacher_id)
            return "teacher deleted successfully."
        
    def search_teacher(self, full_name):
            TeacherValidator.validate_name(full_name)
            teachers = self.teacher_repo.search_teacher(full_name)
            if not teachers:
                raise ValueError("No teachers found.")
            return teachers
    
    def count_teachers(self):
            return self.teacher_repo.count_teacher()
# ===== END controllers/teacher_controller.py =====


# ===== BEGIN repositories/teacher_repository.py =====
from models.teacher import Teacher


class TeacherRepo:

    def __init__(self, db):
        self.db = db

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                phone_number TEXT
            )
        """)

        self.db.connection.commit()


    def add_teacher(self, teacher):

        self.db.cursor.execute("""
            INSERT INTO teachers
            (full_name, email, password, phone_number)
            VALUES (?, ?, ?, ?)
        """, (
            teacher.full_name,
            teacher.email,
            teacher.password,
            teacher.phone_number
        ))

        self.db.connection.commit()

        teacher.teacher_id = self.db.cursor.lastrowid


    def get_teacher(self, teacher_id):

        self.db.cursor.execute("""
            SELECT teacher_id, full_name, email,
                   password, phone_number
            FROM teachers
            WHERE teacher_id = ?
        """, (teacher_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        return Teacher(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4]
        )


    def get_all_teachers(self):

        self.db.cursor.execute("""
            SELECT teacher_id, full_name, email,
                   password, phone_number
            FROM teachers
        """)

        rows = self.db.cursor.fetchall()

        teachers = []

        for row in rows:
            teacher = Teacher(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            )

            teachers.append(teacher)

        return teachers


    def update_teacher(self, teacher_id, **kwargs):

        if "full_name" in kwargs:

            self.db.cursor.execute("""
                UPDATE teachers
                SET full_name = ?
                WHERE teacher_id = ?
            """, (kwargs["full_name"], teacher_id))


        if "email" in kwargs:

            self.db.cursor.execute("""
                UPDATE teachers
                SET email = ?
                WHERE teacher_id = ?
            """, (kwargs["email"], teacher_id))


        if "password" in kwargs:

            self.db.cursor.execute("""
                UPDATE teachers
                SET password = ?
                WHERE teacher_id = ?
            """, (kwargs["password"], teacher_id))


        if "phone_number" in kwargs:

            self.db.cursor.execute("""
                UPDATE teachers
                SET phone_number = ?
                WHERE teacher_id = ?
            """, (kwargs["phone_number"], teacher_id))


        self.db.connection.commit()

        return True


    def delete_teacher(self, teacher_id):

        teacher = self.get_teacher(teacher_id)

        if teacher is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM teachers
            WHERE teacher_id = ?
        """, (teacher_id,))

        self.db.connection.commit()

        return True


    def search_teacher(self, full_name):

        self.db.cursor.execute("""
            SELECT teacher_id, full_name, email,
                   password, phone_number
            FROM teachers
            WHERE full_name LIKE ?
        """, (f"%{full_name}%",))

        rows = self.db.cursor.fetchall()

        teachers = []

        for row in rows:
            teacher = Teacher(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4]
            )

            teachers.append(teacher)

        return teachers


    def count_teacher(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM teachers
        """)

        result = self.db.cursor.fetchone()

        return result[0]

    def get_teacher_by_email(self, email):

        self.db.cursor.execute("""
            SELECT
                teacher_id,
                full_name,
                email,
                password,
                phone_number
            FROM teachers
            WHERE email = ?
        """, (email,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        return Teacher(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4]
        )
# ===== END repositories/teacher_repository.py =====


# ===== BEGIN api/routes/teacher_router.py =====
from fastapi import APIRouter, HTTPException

from api.schemas.teacher_schema import (
    TeacherResponse,
    TeacherCreate,
    TeacherUpdate
)

from api.dependencies import teacher_controller


router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)


@router.get("/", response_model=list[TeacherResponse])
def get_all_teachers():

    teachers = teacher_controller.get_all_teachers()

    return [
        {
            "teacher_id": teacher.teacher_id,
            "full_name": teacher.full_name,
            "email": teacher.email,
            "phone_number": teacher.phone_number
        }
        for teacher in teachers
    ]


@router.post("/")
def create_teacher(data: TeacherCreate):

    result = teacher_controller.create_teacher(
        data.full_name,
        data.email,
        data.password,
        data.phone_number
    )

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Could not create teacher"
        )

    return {
        "message": result
    }


@router.get("/search")
def search_teachers(full_name: str):

    teachers = teacher_controller.search_teacher(full_name)

    return [
        {
            "teacher_id": teacher.teacher_id,
            "full_name": teacher.full_name,
            "email": teacher.email,
            "phone_number": teacher.phone_number
        }
        for teacher in teachers
    ]


@router.get("/count")
def count_teachers():

    count = teacher_controller.count_teachers()

    return {
        "count": count
    }


@router.put("/{teacher_id}")
def update_teacher(
    teacher_id: int,
    data: TeacherUpdate
):

    teacher = teacher_controller.get_teacher(teacher_id)

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    updates = data.model_dump(exclude_none=True)

    result = teacher_controller.update_teacher(
        teacher_id,
        **updates
    )

    return {
        "message": result
    }


@router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int):

    teacher = teacher_controller.get_teacher(teacher_id)

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    result = teacher_controller.delete_teacher(teacher_id)

    return {
        "message": result
    }


@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(teacher_id: int):

    teacher = teacher_controller.get_teacher(teacher_id)

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return {
        "teacher_id": teacher.teacher_id,
        "full_name": teacher.full_name,
        "email": teacher.email,
        "phone_number": teacher.phone_number
    }
# ===== END api/routes/teacher_router.py =====


# ===== BEGIN api/schemas/teacher_schema.py =====
from pydantic import BaseModel


class TeacherResponse(BaseModel):
    teacher_id : int
    full_name : str
    email : str
    phone_number : str


class TeacherCreate(BaseModel):
    full_name : str
    email : str
    password : str
    phone_number : str

class TeacherUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None
    phone_number: str | None = None
# ===== END api/schemas/teacher_schema.py =====


# ===== BEGIN utils/teacher_validation.py =====
class TeacherValidator:

    @staticmethod
    def validate_name(full_name):
        full_name = full_name.strip()
        if not full_name:
            raise ValueError("full name cannot be empty")
        if len(full_name) < 3:
            raise ValueError("Full name must contain as least 3 characters.")
        if len(full_name) > 100:
            raise ValueError("Full name must not exceed 100 characters.")
        if not all(char.isalpha() or char.isspace() for char in full_name):
            raise ValueError("Full name must contain only letters and spaces")
    @staticmethod
    def validate_email(email):
        email = email.strip()            
        if not email:
            raise ValueError("email cannot be empty")
        if "@" not in email or "." not in email:
            raise ValueError("Email must contrain '@'ro '.'.")
        if email.count("@") != 1:
            raise ValueError("Invalid email address.")
    @staticmethod
    def validate_password(password):  
        password = password.strip()  
        if not password:
            raise ValueError("password cannot be empty")
        if len(password) < 8:
            raise ValueError("invalid")
        if not any(char.isalpha() for char in password):
            raise ValueError("Pasword must contain at least one latter.")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number.")
    @staticmethod  
    def validate_phone_number(phone_number):
        phone_number = phone_number.strip()    
        if not phone_number:
            raise ValueError("Phone number cannot be empty")
        if not phone_number.isdigit() :
             raise ValueError("Phone number not correct.")
        if len(phone_number)!=10:
             raise ValueError("Phone number not correct size.")

# ===== END utils/teacher_validation.py =====


# ===== BEGIN models/course.py =====
class Course:
    def __init__(self, course_id, course_name, teacher, level, semester):
            self.course_id = course_id
            self.course_name = course_name
            self.teacher = teacher
            self.level = level
            self.semester = semester
# ===== END models/course.py =====


# ===== BEGIN controllers/course_controller.py =====
from models.course import Course
from utils.validation_course import CourseValidator

class CourseController:
    def __init__(self, course_repo, teacher_repo):
        self.course_repo = course_repo
        self.teacher_repo = teacher_repo

    def create_course(self, course_name, teacher_id, level, semester):

        CourseValidator.validate_course_name(course_name)
        CourseValidator.Validation_level(level)
        CourseValidator.Validation_semester(semester)
        
        teacher = self.teacher_repo.get_teacher(teacher_id)
        if teacher is None:
            raise ValueError("Teacher not found")
        course = Course(None, course_name, teacher, level, semester)

        self.course_repo.add_course(course)
        return "Course created successfully."

    def get_course(self, course_id):

        if not isinstance(course_id, int):
            raise ValueError("Course ID must be an int")
        course = self.course_repo.get_course(course_id)
        if course is None:
            raise ValueError("Course not found.")
        return course

    def get_all_courses(self):
        return self.course_repo.get_all_courses()

    def update_course(self, course_id, **kwargs):
        course = self.course_repo.get_course(course_id)
        if course is None :
            raise ValueError("Course not found")
        if "course_name" in kwargs:
            CourseValidator.validate_course_name(kwargs["course_name"])
        if "teacher_id" in kwargs:
            teacher = self.teacher_repo.get_teacher(kwargs["teacher_id"])
            if teacher is None:
                raise ValueError("Teacher not found.")
            kwargs["teacher"] = teacher
            del kwargs["teacher_id"] 

        self.course_repo.update_course(course_id, **kwargs)
        return "Course updated successfully."
    def delete_course(self, course_id):
        course = self.course_repo.get_course(course_id)
        if course is None:
            raise ValueError('Course ID not found.')
        self.course_repo.delete_course(course_id)
        return "Course deleted successfully"

    def search_course(self, query):
        query = query.strip()
        if not query:
            raise ValueError("Search query cannot be empty.")

        courses = self.course_repo.search_course(query)
        if not courses:
            raise ValueError("No courses found.")
        return courses

    def count_courses(self):
        return self.course_repo.count_courses()

    def get_courses_by_level(self, level):
        courses = self.course_repo.get_courses_by_level(level)
        return courses
# ===== END controllers/course_controller.py =====


# ===== BEGIN repositories/course_repository.py =====
from models.course import Course


class CourseRepo:

    def __init__(self, db):
        self.db = db

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                teacher_id INTEGER NOT NULL,
                semester TEXT NOT NULL,
                level TEXT NOT NULL,
                FOREIGN KEY (teacher_id)
                    REFERENCES teachers(teacher_id)
            )
        """)

        self.db.connection.commit()


    def add_course(self, course):

        self.db.cursor.execute("""
            INSERT INTO courses
            (course_name, teacher_id, semester, level)
            VALUES (?, ?, ?, ?)
        """, (
            course.course_name,
            course.teacher.teacher_id,
            course.semester,
            course.level
        ))

        self.db.connection.commit()

        course.course_id = self.db.cursor.lastrowid


    def get_course(self, course_id):

        self.db.cursor.execute("""
            SELECT course_id, course_name,
                   teacher_id, semester, level
            FROM courses
            WHERE course_id = ?
        """, (course_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        teacher_id = row[2]

        self.db.cursor.execute("""
            SELECT teacher_id, full_name, email,
                   password, phone_number
            FROM teachers
            WHERE teacher_id = ?
        """, (teacher_id,))

        teacher_row = self.db.cursor.fetchone()

        if teacher_row is None:
            return None

        from models.teacher import Teacher

        teacher = Teacher(
            teacher_row[0],
            teacher_row[1],
            teacher_row[2],
            teacher_row[4],
            teacher_row[3]
        )

        return Course(
            row[0],
            row[1],
            teacher,
            row[3],
            row[4]
        )


    def get_all_courses(self):

        self.db.cursor.execute("""
            SELECT
                courses.course_id,
                courses.course_name,
                courses.semester,
                courses.level,
                teachers.teacher_id,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM courses
            JOIN teachers
            ON courses.teacher_id = teachers.teacher_id
        """)

        rows = self.db.cursor.fetchall()

        courses = []

        from models.teacher import Teacher

        for row in rows:

            teacher = Teacher(
                row[4],  # teacher_id
                row[5],  # full_name
                row[6],  # email
                row[7],  # password
                row[8]   # phone_number
            )

            course = Course(
                row[0],  # course_id
                row[1],  # course_name
                teacher,
                row[3],  # semester
                row[2]   # level
            )

            courses.append(course)

        return courses


    def update_course(self, course_id, **kwargs):

        if "course_name" in kwargs:

            self.db.cursor.execute("""
                UPDATE courses
                SET course_name = ?
                WHERE course_id = ?
            """, (
                kwargs["course_name"],
                course_id
            ))


        if "teacher" in kwargs:

            self.db.cursor.execute("""
                UPDATE courses
                SET teacher_id = ?
                WHERE course_id = ?
            """, (
                kwargs["teacher"].teacher_id,
                course_id
            ))


        if "semester" in kwargs:

            self.db.cursor.execute("""
                UPDATE courses
                SET semester = ?
                WHERE course_id = ?
            """, (
                kwargs["semester"],
                course_id
            ))


        if "level" in kwargs:

            self.db.cursor.execute("""
                UPDATE courses
                SET level = ?
                WHERE course_id = ?
            """, (
                kwargs["level"],
                course_id
            ))


        self.db.connection.commit()

        return True


    def delete_course(self, course_id):

        course = self.get_course(course_id)

        if course is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM courses
            WHERE course_id = ?
        """, (course_id,))

        self.db.connection.commit()

        return True


    def search_course(self, query):

        self.db.cursor.execute("""
            SELECT course_id, course_name,
                   teacher_id, semester, level
            FROM courses
            WHERE course_name LIKE ?
        """, (f"%{query}%",))

        rows = self.db.cursor.fetchall()

        courses = []

        from models.teacher import Teacher

        for row in rows:

            self.db.cursor.execute("""
                SELECT teacher_id, full_name, email,
                       password, phone_number
                FROM teachers
                WHERE teacher_id = ?
            """, (row[2],))

            teacher_row = self.db.cursor.fetchone()

            if teacher_row is None:
                continue

            teacher = Teacher(
                teacher_row[0],
                teacher_row[1],
                teacher_row[2],
                teacher_row[3],
                teacher_row[4]
            )

            courses.append(
                Course(
                    row[0],
                    row[1],
                    teacher,
                    row[4],
                    row[3]
                )
            )

        return courses


    def count_courses(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM courses
        """)

        result = self.db.cursor.fetchone()

        return result[0]


    def get_courses_by_level(self, level):

        level = level.strip().upper()

        self.db.cursor.execute("""
            SELECT course_id, course_name, teacher_id, semester, level
            FROM courses
            WHERE UPPER(TRIM(level)) = ?
        """, (level,))

        matched_rows = self.db.cursor.fetchall()

        from models.teacher import Teacher

        courses = []

        for row in matched_rows:
            teacher_id = row[2]

            self.db.cursor.execute("""
                SELECT teacher_id, full_name, email, password, phone_number
                FROM teachers
                WHERE teacher_id = ?
            """, (teacher_id,))

            teacher_row = self.db.cursor.fetchone()

            if teacher_row is None:
                continue

            teacher = Teacher(
                teacher_row[0],
                teacher_row[1],
                teacher_row[2],
                teacher_row[3],
                teacher_row[4]
            )

            courses.append(
                Course(
                    row[0],        # course_id
                    row[1],        # course_name
                    teacher,
                    row[4],        # level
                    row[3]         # semester
                )
            )

        return courses
# ===== END repositories/course_repository.py =====


# ===== BEGIN api/routes/course_router.py =====
from fastapi import APIRouter, HTTPException

from api.schemas.course_schema import (
    CourseResponse,
    CourseCreate,
    CourseUpdate
)

from api.dependencies import course_controller


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.get("/", response_model=list[CourseResponse])
def get_all_courses():

    courses = course_controller.get_all_courses()

    return [
        {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "teacher_id": course.teacher.teacher_id,
            "semester": course.semester,
            "level": course.level
        }
        for course in courses
    ]


@router.post("/")
def create_course(data: CourseCreate):

    result = course_controller.create_course(
        data.course_name,
        data.teacher_id,
        data.level,
        data.semester
    )

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Could not create course"
        )

    return {
        "message": result
    }


@router.get("/search")
def search_courses(query: str):

    courses = course_controller.search_course(query)

    return [
        {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "teacher_id": course.teacher.teacher_id,
            "semester": course.semester,
            "level": course.level
        }
        for course in courses
    ]


@router.get("/count")
def count_courses():

    count = course_controller.count_courses()

    return {
        "count": count
    }


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int):

    course = course_controller.get_course(course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {
        "course_id": course.course_id,
        "course_name": course.course_name,
        "teacher_id": course.teacher.teacher_id,
        "semester": course.semester,
        "level": course.level
    }


@router.put("/{course_id}")
def update_course(
    course_id: int,
    data: CourseUpdate
):

    course = course_controller.get_course(course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    updates = data.model_dump(exclude_none=True)

    result = course_controller.update_course(
        course_id,
        **updates
    )

    return {
        "message": result
    }


@router.delete("/{course_id}")
def delete_course(course_id: int):

    course = course_controller.get_course(course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    result = course_controller.delete_course(course_id)

    return {
        "message": result
    }
# ===== END api/routes/course_router.py =====


# ===== BEGIN api/schemas/course_schema.py =====
from pydantic import BaseModel


class CourseResponse(BaseModel):
    course_id: int
    course_name: str
    teacher_id: int
    level: str
    semester: str
    


class CourseCreate(BaseModel):
    course_name: str
    teacher_id: int
    level: str
    semester: str
    


class CourseUpdate(BaseModel):
    course_name: str | None = None
    teacher_id: int | None = None
    level: str | None = None
    semester: str | None = None
    
# ===== END api/schemas/course_schema.py =====


# ===== BEGIN models/exercise.py =====
class Exercise:
    def __init__(self, exercise_id, exercise_name, course):
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.course = course
# ===== END models/exercise.py =====


# ===== BEGIN controllers/exercise_controller.py =====
from models.exercise import Exercise
from utils.validation_exercise import ExerciseValidator
from models.exercise import Exercise
class ExerciseController:
    def __init__(self, exercise_repo, course_repo):
        self.exercise_repo = exercise_repo
        self.course_repo = course_repo

    def create_exercise(self, exercise_name, course_id):

        ExerciseValidator.validation_exercise_name(exercise_name)

        #find the course id of the exrcise we need 
        course = self.course_repo.get_course(course_id)
        if course is None:
            raise ValueError("No course found.")
        exercise = Exercise(None, exercise_name, course)

        self.exercise_repo.add_exercise(exercise)
        return "Exercise created successfully."

    def get_exercise(self, exercise_id):

        if not isinstance(exercise_id, int):
            raise ValueError("exercise ID must be an int")
        exercise = self.exercise_repo.get_exercise(exercise_id)
        if exercise is None:
            raise ValueError("exercise not found.")
        return exercise

    def get_all_exercises(self):
        return self.exercise_repo.get_all_exercises()

    def update_exercise(self, exercise_id, **kwargs):
        exercise = self.exercise_repo.get_exercise(exercise_id)
        if exercise is None :
            raise ValueError("exercise not found")
        if "exercise_name" in kwargs:
            ExerciseValidator.validation_exercise_name(kwargs["exercise_name"])
        if "course_id" in kwargs:
            course = self.course_repo.get_course(
                kwargs["course_id"]
            )
            if course is None:
                raise ValueError("Course not found.")
            kwargs["course"] = course
            del kwargs["course_id"]

        self.exercise_repo.update_exercise(exercise_id, **kwargs)
        return "exercise updated successfully."

    
    def delete_exercise(self, exercise_id):
        exercise = self.exercise_repo.get_exercise(exercise_id)
        if exercise is None:
            raise ValueError('exercise ID not found.')
        self.exercise_repo.delete_exercise(exercise_id)
        return "exercise deleted successfully"

    def search_exercise(self, query):
        query = query.strip()
        if not query:
            raise ValueError("Search query cannot be empty.")

        exercises = self.exercise_repo.search_exercise(query)
        if not exercises:
            raise ValueError("No exercise found.")
        return exercises

    def count_exercise(self):
        return self.exercise_repo.count_exercises()

    
    def get_exercises_by_level(self, level):

        ExerciseValidator.validation_level(level)

        return self.exercise_repo.get_exercises_by_level(level)
# ===== END controllers/exercise_controller.py =====


# ===== BEGIN repositories/exercise_repository.py =====
from models.exercise import Exercise
from models.course import Course
from models.teacher import Teacher


class ExerciseRepo:

    def __init__(self, db):
        self.db = db

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
                exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise_name TEXT NOT NULL,
                course_id INTEGER NOT NULL,
                FOREIGN KEY (course_id)
                    REFERENCES courses(course_id)
)
        """)

        self.db.connection.commit()


    def add_exercise(self, exercise):

        self.db.cursor.execute("""
            INSERT INTO exercises
            (exercise_name, course_id, level)
            VALUES (?, ?, ?)
        """, (
            exercise.exercise_name,
            exercise.course.course_id,
            exercise.level
        ))

        self.db.connection.commit()

        exercise.exercise_id = self.db.cursor.lastrowid


    def get_exercise(self, exercise_id):

        self.db.cursor.execute("""
            SELECT
                exercise_id,
                exercise_name,
                course_id,
                level
            FROM exercises
            WHERE exercise_id = ?
        """, (exercise_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        course_id = row[2]

        self.db.cursor.execute("""
            SELECT
                courses.course_id,
                courses.course_name,
                courses.teacher_id,
                courses.semester,
                courses.level,
                teachers.teacher_id,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM courses
            JOIN teachers
                ON courses.teacher_id = teachers.teacher_id
            WHERE courses.course_id = ?
        """, (course_id,))

        course_row = self.db.cursor.fetchone()

        if course_row is None:
            return None

        teacher = Teacher(
            course_row[5],
            course_row[6],
            course_row[7],
            course_row[8],
            course_row[9]
        )

        course = Course(
            course_row[0],
            course_row[1],
            teacher,
            course_row[3],
            course_row[4]
        )

        return Exercise(
            row[0],
            row[1],
            course,
        )


    def get_all_exercises(self):

        self.db.cursor.execute("""
            SELECT
                exercises.exercise_id,
                exercises.exercise_name,
                exercises.level,
                courses.course_id,
                courses.course_name,
                courses.teacher_id,
                courses.semester,
                courses.level,
                teachers.teacher_id,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM exercises

            JOIN courses
                ON exercises.course_id = courses.course_id

            JOIN teachers
                ON courses.teacher_id = teachers.teacher_id
        """)

        rows = self.db.cursor.fetchall()

        exercises = []

        for row in rows:

            teacher = Teacher(
                row[8],
                row[9],
                row[10],
                row[11],
                row[12]
            )

            course = Course(
                row[3],
                row[4],
                teacher,
                row[6],
                row[7]
            )

            exercise = Exercise(
                row[0],
                row[1],
                course,
            )

            exercises.append(exercise)

        return exercises


    def update_exercise(self, exercise_id, **kwargs):

        if "exercise_name" in kwargs:

            self.db.cursor.execute("""
                UPDATE exercises
                SET exercise_name = ?
                WHERE exercise_id = ?
            """, (
                kwargs["exercise_name"],
                exercise_id
            ))


        if "course" in kwargs:

            self.db.cursor.execute("""
                UPDATE exercises
                SET course_id = ?
                WHERE exercise_id = ?
            """, (
                kwargs["course"].course_id,
                exercise_id
            ))


        if "level" in kwargs:

            self.db.cursor.execute("""
                UPDATE exercises
                SET level = ?
                WHERE exercise_id = ?
            """, (
                kwargs["level"],
                exercise_id
            ))


        self.db.connection.commit()

        return True


    def delete_exercise(self, exercise_id):

        exercise = self.get_exercise(exercise_id)

        if exercise is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM exercises
            WHERE exercise_id = ?
        """, (exercise_id,))

        self.db.connection.commit()

        return True


    def search_exercise(self, query):

        self.db.cursor.execute("""
            SELECT
                exercises.exercise_id,
                exercises.exercise_name,
                exercises.level,
                courses.course_id,
                courses.course_name,
                courses.teacher_id,
                courses.semester,
                courses.level,
                teachers.teacher_id,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM exercises

            JOIN courses
                ON exercises.course_id = courses.course_id

            JOIN teachers
                ON courses.teacher_id = teachers.teacher_id

            WHERE exercises.exercise_name LIKE ?
        """, (f"%{query}%",))

        rows = self.db.cursor.fetchall()

        exercises = []

        for row in rows:

            teacher = Teacher(
                row[8],
                row[9],
                row[10],
                row[11],
                row[12]
            )

            course = Course(
                row[3],
                row[4],
                teacher,
                row[6],
                row[7]
            )

            exercise = Exercise(
                row[0],
                row[1],
                course,
            )

            exercises.append(exercise)

        return exercises


    def count_exercises(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM exercises
        """)

        result = self.db.cursor.fetchone()

        return result[0]

    def get_exercises_by_level(self, level):

        level = level.strip().upper()

        self.db.cursor.execute("""
            SELECT
                exercises.exercise_id,
                exercises.exercise_name,
                exercises.level,
                courses.course_id,
                courses.course_name,
                courses.teacher_id,
                courses.semester,
                courses.level,
                teachers.teacher_id,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM exercises

            JOIN courses
                ON exercises.course_id = courses.course_id

            JOIN teachers
                ON courses.teacher_id = teachers.teacher_id

            WHERE UPPER(TRIM(exercises.level)) = ?
        """, (level,))

        rows = self.db.cursor.fetchall()

        exercises = []

        for row in rows:

            teacher = Teacher(
                row[8],
                row[9],
                row[10],
                row[11],
                row[12]
            )

            course = Course(
                row[3],
                row[4],
                teacher,
                row[6],
                row[7]
            )

            exercise = Exercise(
                row[0],
                row[1],
                course,
            )

            exercises.append(exercise)

        return exercises
# ===== END repositories/exercise_repository.py =====


# ===== BEGIN api/routes/exercise_router.py =====
from fastapi import APIRouter, HTTPException

from api.schemas.exercise_schema import (
    ExerciseResponse,
    ExerciseCreate,
    ExerciseUpdate
)

from api.dependencies import exercise_controller


router = APIRouter(
    prefix="/exercises",
    tags=["exercises"]
)


@router.get("/", response_model=list[ExerciseResponse])
def get_all_exercises():

    exercises = exercise_controller.get_all_exercises()

    return [
        {
            "exercise_id": exercise.exercise_id,
            "exercise_name": exercise.exercise_name,
            "course_id": exercise.course.course_id,
        }
        for exercise in exercises
    ]


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int):

    try:
        exercise = exercise_controller.get_exercise(exercise_id)

        return {
            "exercise_id": exercise.exercise_id,
            "exercise_name": exercise.exercise_name,
            "course_id": exercise.course.course_id,
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/")
def create_exercise(data: ExerciseCreate):

    try:

        result = exercise_controller.create_exercise(
            data.exercise_name,
            data.course_id,
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.put("/{exercise_id}")
def update_exercise(
    exercise_id: int,
    data: ExerciseUpdate
):

    try:

        updates = data.model_dump(exclude_none=True)

        result = exercise_controller.update_exercise(
            exercise_id,
            **updates
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.delete("/{exercise_id}")
def delete_exercise(exercise_id: int):

    try:

        result = exercise_controller.delete_exercise(
            exercise_id
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get("/search")
def search_exercises(query: str):

    try:

        exercises = exercise_controller.search_exercise(query)

        return [
            {
                "exercise_id": exercise.exercise_id,
                "exercise_name": exercise.exercise_name,
                "course_id": exercise.course.course_id,
            }
            for exercise in exercises
        ]

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get("/count")
def count_exercises():

    return {
        "count": exercise_controller.count_exercise()
    }
# ===== END api/routes/exercise_router.py =====


# ===== BEGIN api/schemas/exercise_schema.py =====
from pydantic import BaseModel


class ExerciseResponse(BaseModel):
    exercise_id: int
    exercise_name: str
    course_id: int


class ExerciseCreate(BaseModel):
    exercise_name: str
    course_id: int


class ExerciseUpdate(BaseModel):
    exercise_name: str | None = None
    course_id: int | None = None
# ===== END api/schemas/exercise_schema.py =====


# ===== BEGIN models/grad.py =====
class Grade:
    def __init__(self, grade_id, score, student, exercise):
        self.grade_id = grade_id
        self.score = score
        self.student = student
        self.exercise = exercise
# ===== END models/grad.py =====


# ===== BEGIN controllers/grade_controller.py =====
from models.grad import Grade
from models.student import Student
from models.exercise import Exercise
from utils.grade_validation import GradeValidator

class GradeController:
    def __init__(self, grade_repo, student_repo, exercise_repo):
        self.grade_repo = grade_repo
        self.student_repo = student_repo
        self.exercise_repo = exercise_repo

    def create_grade(self, score, student_id, exercise_id):
        # check if the student and exercise from Student and Exercise model 
        GradeValidator.validation_score(score)
        if not isinstance(student_id, int):
            raise ValueError("Invalid student.")
        if not isinstance(exercise_id, int):
            raise ValueError("Invalid exercise")
        student = self.student_repo.get_student(student_id)
        if student is None:
            raise ValueError("Student not found.")

        exercise = self.exercise_repo.get_exercise(exercise_id)
        if exercise is None:
            raise ValueError("exercise not found.")
        # create grade
        grade = Grade(None, score, student, exercise)
        # add the grade
        self.grade_repo.add_grade(grade)
        return "Grade created successfully."

    def get_grade(self, grade_id):
        if not isinstance(grade_id, int):
            raise ValueError("Grade ID must be an int")
        grade = self.grade_repo.get_grade(grade_id)
        if grade is None:
            raise ValueError("Grade not found.")
        return grade

    def get_all_grades(self):
        return self.grade_repo.get_all_grades()

    def update_grade(self, grade_id, **kwargs):
        grade = self.grade_repo.get_grade(grade_id)
        if grade is None:
            raise ValueError("grade not found")
        if "score" in kwargs:
            GradeValidator.validation_score(kwargs["score"])

        self.grade_repo.update_grade(grade_id, **kwargs)
        return "Grade updated succssfully."
        
        

    def delete_grade(self, grade_id):

        grade = self.grade_repo.get_grade(grade_id)
        if grade is None:
            raise ValueError("Grade is nout Found .")
        self.grade_repo.delete_grade(grade_id)
        return "Grade deleted succssfully ."

    def search_grade_by_student(self, student_id):
        #chech if student_id is integer
        if not isinstance(student_id, int):
            raise ValueError("Student ID must be int.")

        #check if grade of student if found and return it 
        grades = self.grade_repo.search_grade_by_student(student_id)
        if not grades :
            raise ValueError("No grade found.")
        return grades
    def search_grade_by_exercise(self, exercise_id):
        if not isinstance(exercise_id, int):
            raise ValueError("exercise ID must be int.")
        
        #check if grade of student if found and return it 
        grades = self.grade_repo.search_grade_by_exercise(exercise_id)
        if not grades :
            raise ValueError("No grade found.")
        return grades

    def count_grades(self):
        return self.grade_repo.count_grades()

    def get_grades_by_student(self, student_id):

        if not isinstance(student_id, int):
            raise ValueError("Student ID must be int.")

        student = self.student_repo.get_student(student_id)

        if student is None:
            raise ValueError("Student not found.")

        return self.grade_repo.search_grade_by_student(student_id)
# ===== END controllers/grade_controller.py =====


# ===== BEGIN repositories/grade_repository.py =====
from models.grad import Grade


class GradeRepo:

    def __init__(self, db, student_repo, exercise_repo):

        self.db = db
        self.student_repo = student_repo
        self.exercise_repo = exercise_repo

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                score REAL NOT NULL,
                student_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,

                FOREIGN KEY (student_id)
                    REFERENCES students(student_id),

                FOREIGN KEY (exercise_id)
                    REFERENCES exercises(exercise_id)
            )
        """)

        self.db.connection.commit()


    def add_grade(self, grade):

        self.db.cursor.execute("""
            INSERT INTO grades
            (score, student_id, exercise_id)
            VALUES (?, ?, ?)
        """, (
            grade.score,
            grade.student.student_id,
            grade.exercise.exercise_id
        ))

        self.db.connection.commit()

        grade.grade_id = self.db.cursor.lastrowid


    def get_grade(self, grade_id):

        self.db.cursor.execute("""
            SELECT
                grade_id,
                score,
                student_id,
                exercise_id
            FROM grades
            WHERE grade_id = ?
        """, (grade_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        student = self.student_repo.get_student(row[2])

        exercise = self.exercise_repo.get_exercise(row[3])

        if student is None or exercise is None:
            return None

        return Grade(
            row[0],
            row[1],
            student,
            exercise
        )


    def get_all_grades(self):

        self.db.cursor.execute("""
            SELECT
                grade_id,
                score,
                student_id,
                exercise_id
            FROM grades
        """)

        rows = self.db.cursor.fetchall()

        grades = []

        for row in rows:

            student = self.student_repo.get_student(row[2])

            exercise = self.exercise_repo.get_exercise(row[3])

            if student is None or exercise is None:
                continue

            grade = Grade(
                row[0],
                row[1],
                student,
                exercise
            )

            grades.append(grade)

        return grades


    def update_grade(self, grade_id, **kwargs):

        if "score" in kwargs:

            self.db.cursor.execute("""
                UPDATE grades
                SET score = ?
                WHERE grade_id = ?
            """, (
                kwargs["score"],
                grade_id
            ))


        if "student" in kwargs:

            self.db.cursor.execute("""
                UPDATE grades
                SET student_id = ?
                WHERE grade_id = ?
            """, (
                kwargs["student"].student_id,
                grade_id
            ))


        if "exercise" in kwargs:

            self.db.cursor.execute("""
                UPDATE grades
                SET exercise_id = ?
                WHERE grade_id = ?
            """, (
                kwargs["exercise"].exercise_id,
                grade_id
            ))


        self.db.connection.commit()

        return True


    def delete_grade(self, grade_id):

        grade = self.get_grade(grade_id)

        if grade is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM grades
            WHERE grade_id = ?
        """, (grade_id,))

        self.db.connection.commit()

        return True


    def search_grade_by_student(self, student_id):

        self.db.cursor.execute("""
            SELECT
                grade_id,
                score,
                student_id,
                exercise_id
            FROM grades
            WHERE student_id = ?
        """, (student_id,))

        rows = self.db.cursor.fetchall()

        grades = []

        for row in rows:

            student = self.student_repo.get_student(row[2])

            exercise = self.exercise_repo.get_exercise(row[3])

            if student is None or exercise is None:
                continue

            grade = Grade(
                row[0],
                row[1],
                student,
                exercise
            )

            grades.append(grade)

        return grades


    def search_grade_by_exercises(self, exercise_id):

        self.db.cursor.execute("""
            SELECT
                grade_id,
                score,
                student_id,
                exercise_id
            FROM grades
            WHERE exercise_id = ?
        """, (exercise_id,))

        rows = self.db.cursor.fetchall()

        grades = []

        for row in rows:

            student = self.student_repo.get_student(row[2])

            exercise = self.exercise_repo.get_exercise(row[3])

            if student is None or exercise is None:
                continue

            grade = Grade(
                row[0],
                row[1],
                student,
                exercise
            )

            grades.append(grade)

        return grades


    def count_grades(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM grades
        """)

        result = self.db.cursor.fetchone()

        return result[0]
# ===== END repositories/grade_repository.py =====


# ===== BEGIN api/routes/grade_router.py =====
from fastapi import APIRouter, HTTPException

from api.schemas.grade_schema import (
    GradeCreate,
    GradeUpdate,
    GradeResponse
)

from api.dependencies import grade_controller


router = APIRouter(
    prefix="/grades",
    tags=["grades"]
)


def grade_to_response(grade):

    return {
        "grade_id": grade.grade_id,
        "score": grade.score,
        "student_id": grade.student.student_id,
        "exercise_id": grade.exercise.exercise_id
    }


@router.post(
    "/",
    response_model=dict
)
def create_grade(data: GradeCreate):

    try:

        result = grade_controller.create_grade(
            data.score,
            data.student_id,
            data.exercise_id
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get(
    "/",
    response_model=list[GradeResponse]
)
def get_all_grades():

    grades = grade_controller.get_all_grades()

    return [
        grade_to_response(grade)
        for grade in grades
    ]


@router.get(
    "/student/{student_id}",
    response_model=list[GradeResponse]
)
def get_grades_by_student(student_id: int):

    try:

        grades = (
            grade_controller
            .search_grade_by_student(student_id)
        )

        return [
            grade_to_response(grade)
            for grade in grades
        ]

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get(
    "/exercise/{exercise_id}",
    response_model=list[GradeResponse]
)
def get_grades_by_exercise(exercise_id: int):

    try:

        grades = (
            grade_controller
            .search_grade_by_exercise(exercise_id)
        )

        return [
            grade_to_response(grade)
            for grade in grades
        ]

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@router.get(
    "/count",
    response_model=dict
)
def count_grades():

    return {
        "count": grade_controller.count_grades()
    }

@router.get(
    "/{grade_id}",
    response_model=GradeResponse
)
def get_grade(grade_id: int):

    try:

        grade = grade_controller.get_grade(
            grade_id
        )

        return grade_to_response(grade)

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.put(
    "/{grade_id}",
    response_model=dict
)
def update_grade(
    grade_id: int,
    data: GradeUpdate
):

    try:

        updates = data.model_dump(
            exclude_none=True
        )

        result = grade_controller.update_grade(
            grade_id,
            **updates
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.delete(
    "/{grade_id}",
    response_model=dict
)
def delete_grade(grade_id: int):

    try:

        result = grade_controller.delete_grade(
            grade_id
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
# ===== END api/routes/grade_router.py =====


# ===== BEGIN api/schemas/grade_schema.py =====
from pydantic import BaseModel


class GradeCreate(BaseModel):
    score: float
    student_id: int
    exercise_id: int


class GradeUpdate(BaseModel):
    score: float | None = None


class GradeResponse(BaseModel):
    grade_id: int
    score: float
    student_id: int
    exercise_id: int
# ===== END api/schemas/grade_schema.py =====


# ===== BEGIN models/submission.py =====
class Submission:
    def __init__(self, submission_id, student_id, exercise, submission_date, file_path, status):
        self.submission_id = submission_id  
        self.student_id = student_id
        self.exercise = exercise
        self.submission_date = submission_date
        self.file_path = file_path
        self.status = status
# ===== END models/submission.py =====


# ===== BEGIN controllers/submission_controller.py =====
from models.student import Student
from models.exercise import Exercise
from utils.submission_validation import SubmissionValidator
from models.submission import Submission
from datetime import datetime



class SubmissionController:
    def __init__(self, submission_repo, student_repo, exercise_repo):
        self.submission_repo = submission_repo
        self.student_repo = student_repo
        self.exercise_repo = exercise_repo

    def create_submission(self, student_id, exercise_id, file_path):

        if not isinstance(student_id, int):
            raise ValueError("Invalid student")

        if not isinstance(exercise_id, int):
            raise ValueError("Invalid exercise")

        student = self.student_repo.get_student(student_id)

        if student is None:
            raise ValueError("Student not found.")

        exercise = self.exercise_repo.get_exercise(exercise_id)

        if exercise is None:
            raise ValueError("Exercise not found.")

        submission_date = datetime.now()

        status = "submitted"

        submission = Submission(
            None,
            student_id,
            exercise,
            submission_date,
            file_path,
            status
        )

        self.submission_repo.add_submission(submission)

        return submission
    def get_submission(self, submission_id):
        if not isinstance(submission_id, int):
            raise ValueError("Submission ID mustbe int.")
        submission = self.submission_repo.get_submission(submission_id)
        if submission is None:
            raise ValueError("Submition not found")
        return submission
    def get_all_submissions(self):
        return self.submission_repo.get_all_submissions()

    def update_submission(self, submission_id, **kwargs):
        submission = self.submission_repo.get_submission(submission_id)
        if submission is None:
            raise ValueError("Submission not found.")
        if "status" in kwargs:
            SubmissionValidator.validation_status(kwargs["status"])

        self.submission_repo.update_submission(submission_id, **kwargs)
        return "Submission updated successfully"
    
    def delete_submission(self, submission_id):
        if not isinstance(submission_id, int):
            raise ValueError("Submission ID must be int")
        submission = self.submission_repo.get_submission(submission_id)
        if submission is None:
            raise ValueError("Submission not found.")
        self.submission_repo.delete_submission(submission_id)
        return "Submission deleted succssefully."

    def search_submission_by_student(self, student_id):
        if not isinstance(student_id, int):
            raise ValueError("Student ID must be int.")
        student = self.student_repo.get_student(student_id)
        if student is None:
            raise ValueError("Student not found.")
        submissions = self.submission_repo.search_submission_by_student(student_id)
        if submissions is None:
            raise ValueError("Submission not found.")
        return submissions


    def search_submission_by_exercise(self, exercise_id):
        if not isinstance(exercise_id, int):
            raise ValueError("exercise ID must be int.")
        exercise = self.exercise_repo.get_exercise(exercise_id)
        if exercise is None:
            raise ValueError("exercise not found.")
        submissions = self.submission_repo.search_submission_by_exercise(exercise_id)
        if not submissions :
            raise ValueError("Submission not found.")
        return submissions

    
    def count_submissions(self):
        return self.submission_repo.count_submissions()

    def get_submissions_by_student(self, student_id):

        if not isinstance(student_id, int):
            raise ValueError("Student ID must be int.")

        student = self.student_repo.get_student(student_id)

        if student is None:
            raise ValueError("Student not found.")

        return self.submission_repo.get_submissions_by_student(student_id)
# ===== END controllers/submission_controller.py =====


# ===== BEGIN repositories/submission_repository.py =====
from models.submission import Submission
from models.exercise import Exercise
from models.course import Course
from models.teacher import Teacher
from models.student import Student


class SubmissionRepo:

    def __init__(self, db, student_repo, exercise_repo):
        self.db = db
        self.student_repo = student_repo
        self.exercise_repo = exercise_repo

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                exercise_id INTEGER NOT NULL,
                submission_date TEXT NOT NULL,
                file_path TEXT NOT NULL,
                status TEXT NOT NULL,

                FOREIGN KEY (student_id)
                    REFERENCES students(student_id),

                FOREIGN KEY (exercise_id)
                    REFERENCES exercises(exercise_id)
            )
        """)

        self.db.connection.commit()


    def add_submission(self, submission):

        self.db.cursor.execute("""
            INSERT INTO submissions
            (
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            submission.student_id,
            submission.exercise.exercise_id,
            submission.submission_date,
            submission.file_path,
            submission.status
        ))

        self.db.connection.commit()

        submission.submission_id = self.db.cursor.lastrowid


    def get_submission(self, submission_id):

        self.db.cursor.execute("""
            SELECT
                submission_id,
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            FROM submissions
            WHERE submission_id = ?
        """, (submission_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        student = self.student_repo.get_student(row[1])

        exercise = self.exercise_repo.get_exercise(row[2])

        if student is None or exercise is None:
            return None

        return Submission(
            row[0],
            student.student_id,
            exercise,
            row[3],
            row[4],
            row[5]
        )


    def get_all_submissions(self):

        self.db.cursor.execute("""
            SELECT
                submission_id,
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            FROM submissions
        """)

        rows = self.db.cursor.fetchall()

        submissions = []

        for row in rows:

            student = self.student_repo.get_student(row[1])

            exercise = self.exercise_repo.get_exercise(row[2])

            if student is None or exercise is None:
                continue

            submission = Submission(
                row[0],
                student.student_id,
                exercise,
                row[3],
                row[4],
                row[5]
            )

            submissions.append(submission)

        return submissions


    def update_submission(self, submission_id, **kwargs):

        if "student_id" in kwargs:

            self.db.cursor.execute("""
                UPDATE submissions
                SET student_id = ?
                WHERE submission_id = ?
            """, (
                kwargs["student_id"],
                submission_id
            ))


        if "exercise" in kwargs:

            self.db.cursor.execute("""
                UPDATE submissions
                SET exercise_id = ?
                WHERE submission_id = ?
            """, (
                kwargs["exercise"].exercise_id,
                submission_id
            ))


        if "submission_date" in kwargs:

            self.db.cursor.execute("""
                UPDATE submissions
                SET submission_date = ?
                WHERE submission_id = ?
            """, (
                kwargs["submission_date"],
                submission_id
            ))


        if "file_path" in kwargs:

            self.db.cursor.execute("""
                UPDATE submissions
                SET file_path = ?
                WHERE submission_id = ?
            """, (
                kwargs["file_path"],
                submission_id
            ))


        if "status" in kwargs:

            self.db.cursor.execute("""
                UPDATE submissions
                SET status = ?
                WHERE submission_id = ?
            """, (
                kwargs["status"],
                submission_id
            ))


        self.db.connection.commit()

        return True


    def delete_submission(self, submission_id):

        submission = self.get_submission(submission_id)

        if submission is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM submissions
            WHERE submission_id = ?
        """, (submission_id,))

        self.db.connection.commit()

        return True


    def search_submission_by_student(self, student_id):

        self.db.cursor.execute("""
            SELECT
                submission_id,
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            FROM submissions
            WHERE student_id = ?
        """, (student_id,))

        rows = self.db.cursor.fetchall()

        submissions = []

        for row in rows:

            exercise = self.exercise_repo.get_exercise(row[2])

            if exercise is None:
                continue

            submission = Submission(
                row[0],
                row[1],
                exercise,
                row[3],
                row[4],
                row[5]
            )

            submissions.append(submission)

        return submissions


    def search_submission_by_exercise(self, exercise_id):

        self.db.cursor.execute("""
            SELECT
                submission_id,
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            FROM submissions
            WHERE exercise_id = ?
        """, (exercise_id,))

        rows = self.db.cursor.fetchall()

        submissions = []

        for row in rows:

            submission = Submission(
                row[0],
                row[1],
                self.exercise_repo.get_exercise(row[2]),
                row[3],
                row[4],
                row[5]
            )

            submissions.append(submission)

        return submissions


    def count_submissions(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM submissions
        """)

        result = self.db.cursor.fetchone()

        return result[0]

    def get_submissions_by_student(self, student_id):

        self.db.cursor.execute("""
            SELECT
                submission_id,
                student_id,
                exercise_id,
                submission_date,
                file_path,
                status
            FROM submissions
            WHERE student_id = ?
        """, (student_id,))

        rows = self.db.cursor.fetchall()

        submissions = []

        for row in rows:

            exercise = self.exercise_repo.get_exercise(row[2])

            if exercise is None:
                continue

            submission = Submission(
                row[0],
                row[1],
                exercise,
                row[3],
                row[4],
                row[5]
            )

            submissions.append(submission)

        return submissions
# ===== END repositories/submission_repository.py =====


# ===== BEGIN api/routes/submission_router.py =====
from fastapi import APIRouter, HTTPException

from api.schemas.submission_schema import (
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionResponse
)

from api.dependencies import submission_controller


router = APIRouter(
    prefix="/submissions",
    tags=["submissions"]
)


def submission_to_response(submission):

    return {
        "submission_id": submission.submission_id,
        "student_id": submission.student_id,
        "exercise_id": submission.exercise.exercise_id,
        "submission_date": submission.submission_date,
        "file_path": submission.file_path,
        "status": submission.status
    }


@router.post(
    "/",
    response_model=dict
)
def create_submission(data: SubmissionCreate):

    try:

        result = submission_controller.create_submission(
            data.student_id,
            data.exercise_id,
            data.submission_date,
            data.file_path,
            data.status
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get(
    "/",
    response_model=list[SubmissionResponse]
)
def get_all_submissions():

    submissions = (
        submission_controller
        .get_all_submissions()
    )

    return [
        submission_to_response(submission)
        for submission in submissions
    ]


@router.get(
    "/student/{student_id}",
    response_model=list[SubmissionResponse]
)
def get_submissions_by_student(
    student_id: int
):

    try:

        submissions = (
            submission_controller
            .search_submission_by_student(
                student_id
            )
        )

        return [
            submission_to_response(submission)
            for submission in submissions
        ]

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@router.get(
    "/exercise/{exercise_id}",
    response_model=list[SubmissionResponse]
)
def get_submissions_by_exercise(
    exercise_id: int
):

    try:

        submissions = (
            submission_controller
            .search_submission_by_exercise(
                exercise_id
            )
        )

        return [
            submission_to_response(submission)
            for submission in submissions
        ]

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@router.get(
    "/count",
    response_model=dict
)
def count_submissions():

    return {
        "count":
            submission_controller
            .count_submissions()
    }

@router.get(
    "/{submission_id}",
    response_model=SubmissionResponse
)
def get_submission(
    submission_id: int
):

    try:

        submission = (
            submission_controller
            .get_submission(
                submission_id
            )
        )

        return submission_to_response(
            submission
        )

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@router.put(
    "/{submission_id}",
    response_model=dict
)
def update_submission(
    submission_id: int,
    data: SubmissionUpdate
):

    try:

        updates = data.model_dump(
            exclude_none=True
        )

        result = (
            submission_controller
            .update_submission(
                submission_id,
                **updates
            )
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.delete(
    "/{submission_id}",
    response_model=dict
)
def delete_submission(
    submission_id: int
):

    try:

        result = (
            submission_controller
            .delete_submission(
                submission_id
            )
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
# ===== END api/routes/submission_router.py =====


# ===== BEGIN api/schemas/submission_schema.py =====
from pydantic import BaseModel
from datetime import datetime


class SubmissionCreate(BaseModel):
    exercise_id: int
    file_path: str

class SubmissionUpdate(BaseModel):
    submission_date: datetime | None = None
    file_path: str | None = None
    status: str | None = None


class SubmissionResponse(BaseModel):
    submission_id: int
    student_id: int
    exercise_id: int
    submission_date: datetime
    file_path: str
    status: str
# ===== END api/schemas/submission_schema.py =====


# ===== BEGIN models/notification.py =====
class Notification:
    def __init__(self, notification_id, title, message, sender, receiver, created_at=None):
            self.notification_id = notification_id
            self.title = title
            self.message = message
            self.sender = sender
            self.receiver = receiver
            self.created_at = created_at
# ===== END models/notification.py =====


# ===== BEGIN controllers/notification_controller.py =====
from utils.notification_validation import NotificationValidator
from models.notification import Notification
from models.teacher import Teacher
from models.student import Student
from datetime import datetime
from models.student_notification import StudentNotification




class NotificationController:
    def __init__(self, notification_repo,student_notification_repo ,teacher_repo, student_repo):
        self.notification_repo = notification_repo
        self.student_notification_repo = student_notification_repo
        self.teacher_repo = teacher_repo
        self.student_repo = student_repo

    def create_notification(self, title, message, teacher_id):

        NotificationValidator.validation_title(title)
        NotificationValidator.validation_message(message)

        created_at = datetime.now()
        teacher = self.teacher_repo.get_teacher(teacher_id)
        if not isinstance(teacher_id, int):
            raise ValueError("Teacher ID must be an integer.")
        if teacher is None:
            raise ValueError("Teacher not found.")
    
        notification = Notification(None, title, message, teacher, created_at)
        self.notification_repo.add_notification(notification)
        return notification

    
    def send_to_all_students(self, notification):

        students = self.student_repo.get_all_student()
        if not students:
            raise ValueError("No students found.")

        for student in students:
            student_notification = StudentNotification(
                None,
                student,
                notification
            )
            self.student_notification_repo.add_student_notification(
                student_notification
            )

        return "Notification sent to all students."

    def send_to_student(self, notification, student_id):
        if not isinstance(student_id, int):
            raise ValueError("Student ID must be an integer.")
        student = self.student_repo.get_student(student_id)
        if student is None:
            raise ValueError("Student not found.")
        student_notification = StudentNotification(None, student, notification)
        self.student_notification_repo.add_student_notification(student_notification)
        return "Notification sent to student."


    def get_notification(self, notification_id):

        if not isinstance(notification_id, int):
            raise ValueError("notification ID mustbe int.")
        notification = self.notification_repo.get_notification(notification_id)
        if notification is None:
            raise ValueError("notification not found")
        return notification

    
    def get_all_notifications(self):
        return self.notification_repo.get_all_notifications()

    def get_student_notifications(self, student_id):

        # validation student id
        if not isinstance(student_id, int):
            raise ValueError(
                "Student ID must be an integer."
            )

        student = self.student_repo.get_student(student_id)
        if student is None:
            raise ValueError(
                "Student not found."
            )

        return self.student_notification_repo.get_notifications_for_student(
            student_id
        )

    def mark_as_read(self, student_notification_id):

        if not isinstance(student_notification_id, int):
            raise ValueError(
                "Student Notification ID must be an integer."
            )
        result = self.student_notification_repo.mark_as_read(
            student_notification_id
        )
        if not result:
            raise ValueError(
                "Student notification not found."
            )
        return "Notification marked as read."

    
# ===== END controllers/notification_controller.py =====


# ===== BEGIN repositories/notification_repository.py =====
from models.notification import Notification
from models.teacher import Teacher


class NotificationRepo:

    def __init__(self, db):
        self.db = db

        self.db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                sender_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (sender_id)
                    REFERENCES teachers(teacher_id)
            )
        """)

        self.db.connection.commit()


    def add_notification(self, notification):

        self.db.cursor.execute("""
            INSERT INTO notifications
            (title, message, sender_id, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            notification.title,
            notification.message,
            notification.sender.teacher_id
        ))

        self.db.connection.commit()

        notification.notification_id = self.db.cursor.lastrowid


    def get_notification(self, notification_id):

        self.db.cursor.execute("""
            SELECT
                notifications.notification_id,
                notifications.title,
                notifications.message,
                notifications.sender_id,
                notifications.created_at,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM notifications

            JOIN teachers
                ON notifications.sender_id = teachers.teacher_id

            WHERE notifications.notification_id = ?
        """, (notification_id,))

        row = self.db.cursor.fetchone()

        if row is None:
            return None

        teacher = Teacher(
            row[3],
            row[5],
            row[6],
            row[7],
            row[8]
        )

        return Notification(
            row[0],
            row[1],
            row[2],
            teacher,
            None,
            row[4]
        )


    def get_all_notifications(self):

        self.db.cursor.execute("""
            SELECT
                notifications.notification_id,
                notifications.title,
                notifications.message,
                notifications.sender_id,
                notifications.created_at,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM notifications

            JOIN teachers
                ON notifications.sender_id = teachers.teacher_id
        """)

        rows = self.db.cursor.fetchall()

        notifications = []

        for row in rows:

            teacher = Teacher(
                row[3],
                row[5],
                row[6],
                row[7],
                row[8]
            )

            notification = Notification(
                                row[0],
                                row[1],
                                row[2],
                                teacher,
                                None,
                                row[4]
                            )

            notifications.append(notification)

        return notifications


    def update_notification(self, notification_id, **kwargs):

        if "title" in kwargs:

            self.db.cursor.execute("""
                UPDATE notifications
                SET title = ?
                WHERE notification_id = ?
            """, (
                kwargs["title"],
                notification_id
            ))


        if "message" in kwargs:

            self.db.cursor.execute("""
                UPDATE notifications
                SET message = ?
                WHERE notification_id = ?
            """, (
                kwargs["message"],
                notification_id
            ))


        if "sender" in kwargs:

            self.db.cursor.execute("""
                UPDATE notifications
                SET sender_id = ?
                WHERE notification_id = ?
            """, (
                kwargs["sender"].teacher_id,
                notification_id
            ))


        if "created_at" in kwargs:

            self.db.cursor.execute("""
                UPDATE notifications
                SET created_at = ?
                WHERE notification_id = ?
            """, (
                kwargs["created_at"],
                notification_id
            ))


        self.db.connection.commit()

        return True


    def delete_notification(self, notification_id):

        notification = self.get_notification(notification_id)

        if notification is None:
            return False

        self.db.cursor.execute("""
            DELETE FROM notifications
            WHERE notification_id = ?
        """, (notification_id,))

        self.db.connection.commit()

        return True


    def search_notification(self, query):

        self.db.cursor.execute("""
            SELECT
                notifications.notification_id,
                notifications.title,
                notifications.message,
                notifications.sender_id,
                notifications.created_at,
                teachers.full_name,
                teachers.email,
                teachers.password,
                teachers.phone_number
            FROM notifications

            JOIN teachers
                ON notifications.sender_id = teachers.teacher_id

            WHERE notifications.title LIKE ?
               OR notifications.message LIKE ?
        """, (
            f"%{query}%",
            f"%{query}%"
        ))

        rows = self.db.cursor.fetchall()

        notifications = []

        for row in rows:

            teacher = Teacher(
                row[3],
                row[5],
                row[6],
                row[7],
                row[8]
            )

            notification = Notification(
                    row[0],
                    row[1],
                    row[2],
                    teacher,
                    None,
                    row[4]
                )

            notifications.append(notification)

        return notifications


    def count_notifications(self):

        self.db.cursor.execute("""
            SELECT COUNT(*)
            FROM notifications
        """)

        result = self.db.cursor.fetchone()

        return result[0]
# ===== END repositories/notification_repository.py =====


# ===== BEGIN api/routes/notification_router.py =====
from fastapi import APIRouter, HTTPException

from api.schemas.notification_schema import (
    NotificationResponse,
    NotificationCreate,
    NotificationUpdate
)

from api.dependencies import notification_controller


router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)


def notification_to_response(notification):

    return {
        "notification_id": notification.notification_id,
        "title": notification.title,
        "message": notification.message,
        "teacher_id": notification.sender.teacher_id,
        "teacher_name": notification.sender.full_name,
        "created_at": notification.created_at
    }

@router.get("/", response_model=list[NotificationResponse])
def get_all_notifications():

    notifications = notification_controller.get_all_notifications()

    return [
        notification_to_response(notification)
        for notification in notifications
    ]

@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(notification_id: int):

    try:

        notification = notification_controller.get_notification(
            notification_id
        )

        return notification_to_response(notification)

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

@router.post("/")
def create_notification(data: NotificationCreate):

    try:
        notification = notification_controller.create_notification(
            data.title,
            data.message,
            data.teacher_id
        )

        result = notification_controller.send_to_student(
            notification,
            data.student_id
        )

        return {
            "message": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    
@router.put("/{notification_id}")
def update_notification(
    notification_id: int,
    data: NotificationUpdate
):

    try:

        updates = data.model_dump(exclude_none=True)

        result = notification_controller.update_notification(
            notification_id,
            **updates
        )

        return {
            "message": result
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@router.get("/search")
def search_notifications(query: str):

    try:

        notifications = notification_controller.search_notification(
            query
        )

        return [
            notification_to_response(notification)
            for notification in notifications
        ]

    except ValueError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get("/count")
def count_notifications():

    return {
        "count": notification_controller.count_notifications()
    }
# ===== END api/routes/notification_router.py =====


# ===== BEGIN api/schemas/notification_schema.py =====
from pydantic import BaseModel


class NotificationResponse(BaseModel):
    notification_id: int
    title: str
    message: str
    teacher_id: int
    teacher_name: str
    created_at: str


class NotificationCreate(BaseModel):
    title: str
    message: str
    teacher_id: int
    student_id: int


class NotificationUpdate(BaseModel):
    title: str | None = None
    message: str | None = None
    teacher_id: int | None = None
# ===== END api/schemas/notification_schema.py =====


# ===== BEGIN api/dependencies.py =====
from database.database import Database

from repositories.student_repository import StudentRepo
from controllers.student_controller import StudentController

from repositories.teacher_repository import TeacherRepo
from controllers.teacher_controller import TeacherController

from repositories.course_repository import CourseRepo
from controllers.course_controller import CourseController

from repositories.exercise_repository import ExerciseRepo
from controllers.exercise_controller import ExerciseController

from controllers.notification_controller import NotificationController
from repositories.notification_repository import NotificationRepo
from repositories.student_notification_repository import StudentNotificationRepo

from repositories.submission_repository import SubmissionRepo
from controllers.submission_controller import SubmissionController

from repositories.grade_repository import GradeRepo
from controllers.grade_controller import GradeController

from controllers.auth_controller import AuthController
db = Database()

# Student
student_repo = StudentRepo(db)
student_controller = StudentController(student_repo)

# Teacher
teacher_repo = TeacherRepo(db)
teacher_controller = TeacherController(teacher_repo)

# Course
course_repo = CourseRepo(db)
course_controller = CourseController(
    course_repo,
    teacher_repo
)

exercise_repo = ExerciseRepo(db)
exercise_controller = ExerciseController(exercise_repo, course_repo)

notification_repo = NotificationRepo(db)

student_notification_repo = StudentNotificationRepo(
    db,
    student_repo,
    notification_repo
)

notification_controller = NotificationController(
    notification_repo,
    student_notification_repo,
    teacher_repo,
    student_repo
)

submission_repo = SubmissionRepo(
    db,
    student_repo,
    exercise_repo
)
submission_controller = SubmissionController(
    submission_repo,
    student_repo,
    exercise_repo
)

grade_repo = GradeRepo(db, student_repo, exercise_repo)

grade_controller = GradeController(
    grade_repo,
    student_repo,
    exercise_repo
)

auth_controller= AuthController(
    student_repo,
    teacher_repo
)

"""
create :
get_current_user()
require_student()
require_teacher()

"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from utils.security import decode_access_token
security = HTTPBearer()
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None or role is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user_id = int(user_id)

        if role == "student":
            user = student_repo.get_student(user_id)

        elif role == "teacher":
            user = teacher_repo.get_teacher(user_id)

        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid role"
            )

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def require_student(current_user=Depends(get_current_user)):

    if not hasattr(current_user, "student_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student access required"
        )

    return current_user


def require_teacher(current_user=Depends(get_current_user)):

    if not hasattr(current_user, "teacher_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher access required"
        )

    return current_user


# ===== END api/dependencies.py =====


# ===== BEGIN api/schemas/auth_schema.py =====
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
# ===== END api/schemas/auth_schema.py =====


# ===== BEGIN utils/security.py =====
from datetime import datetime, timedelta, timezone

from jose import jwt
from pwdlib import PasswordHash


SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict):

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({
        "exp": expire
    })

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token: str):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
# ===== END utils/security.py =====


# ===== BEGIN api/routes/auth_router.py =====
from fastapi import APIRouter, HTTPException

from api.schemas.auth_schema import (
    LoginRequest,
    LoginResponse
)

from api.dependencies import auth_controller


router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):

    result = auth_controller.login(
        data.email,
        data.password
    )

    if result is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return result
# ===== END api/routes/auth_router.py =====

