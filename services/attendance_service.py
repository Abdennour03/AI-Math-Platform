from datetime import date


class AttendanceService:
    VALID_STATUSES = {"present", "absent"}

    def __init__(self, attendance_repo, teacher_repo, class_service):
        self.attendance_repo = attendance_repo
        self.teacher_repo = teacher_repo
        self.class_service = class_service

    def get_class_students(self, teacher_id, class_id):
        self._require_teacher_class(teacher_id, class_id)
        return self.attendance_repo.get_students_by_class(class_id)

    def save_attendance(self, teacher_id, class_id, attendance_date, records):
        self._require_teacher_class(teacher_id, class_id)
        if not records:
            raise ValueError("Attendance records are required.")
        if any(record["status"] not in self.VALID_STATUSES for record in records):
            raise ValueError("Attendance status must be present or absent.")
        if len({record["student_id"] for record in records}) != len(records):
            raise ValueError("Each student can appear only once per attendance date.")

        students = self.attendance_repo.get_students_by_class(class_id)
        class_student_ids = {student["student_id"] for student in students}
        submitted_ids = {record["student_id"] for record in records}
        if not submitted_ids <= class_student_ids:
            raise ValueError("All students must belong to the selected class.")

        self.attendance_repo.save_attendance(class_id, attendance_date.isoformat(), records)
        return {"message": "Attendance saved successfully."}

    def get_teacher_history(self, teacher_id, class_id=None, month=None):
        if class_id is not None:
            self._require_teacher_class(teacher_id, class_id)
        self._validate_month(month)
        return self.attendance_repo.get_teacher_history(teacher_id, class_id, month)

    def get_monthly_report(self, class_id, month):
        self.class_service.get_class(class_id)
        self._validate_month(month)
        return self.attendance_repo.get_monthly_report(class_id, month)

    def _require_teacher_class(self, teacher_id, class_id):
        self.class_service.get_class(class_id)
        if self.teacher_repo.get_teacher_id_for_class(class_id) != teacher_id:
            raise ValueError("You can only manage attendance for your assigned classes.")

    @staticmethod
    def _validate_month(month):
        if month is None:
            return
        try:
            date.fromisoformat(f"{month}-01")
        except ValueError as error:
            raise ValueError("Month must use YYYY-MM format.") from error
