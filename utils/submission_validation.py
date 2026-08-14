class SubmissionValidator:
    @staticmethod
    def validation_status(status):
        status = status.strip().lower()
        allowed_status = {
            "submitted",
            "late",
            "graded"
        }
        if status not in allowed_status:
            raise ValueError("Invalid submission status.")
        