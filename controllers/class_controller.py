class ClassController:
    def __init__(self, class_service):
        self.class_service = class_service

    def create_class(self, name, academic_year):
        return self.class_service.create_class(name, academic_year)

    def get_class(self, class_id):
        return self.class_service.get_class(class_id)

    def get_all_classes(self):
        return self.class_service.get_all_classes()

    def search_classes(self, query):
        return self.class_service.search_classes(query)

    def update_class(self, class_id, **updates):
        return self.class_service.update_class(class_id, **updates)

    def delete_class(self, class_id):
        return self.class_service.delete_class(class_id)