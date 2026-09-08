class AdminController:
    def __init__(self, admin_service):
        self.admin_service = admin_service

    def create_student(self, data):
        return self.admin_service.create_student(data)

    def setup_admin(self, full_name, email, password):
        return self.admin_service.setup_admin(full_name, email, password)

    def create_teacher(self, data):
        return self.admin_service.create_teacher(data)

    def update_student(self, student_id, updates):
        return self.admin_service.update_student(student_id, updates)

    def update_teacher(self, teacher_id, updates):
        return self.admin_service.update_teacher(teacher_id, updates)

    def get_student_report(self, student_id):
        return self.admin_service.get_student_report(student_id)

    def get_profile(self, admin_id):
        return self.admin_service.get_profile(admin_id)

    def update_profile(self, admin_id, updates):
        return self.admin_service.update_profile(admin_id, updates)

    def assign_student_to_class(self, student_id, class_id):
        return self.admin_service.assign_student_to_class(student_id, class_id)

    def assign_teacher_to_classes(self, teacher_id, class_ids):
        return self.admin_service.assign_teacher_to_classes(teacher_id, class_ids)