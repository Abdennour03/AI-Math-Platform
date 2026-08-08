class StudentValidator:

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
            raise ValueError("invalid size of password")
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
    @staticmethod    
    def validate_level(level): 
        level = level.strip()   
        allowed_levels = {"3AC", "TRC", "1BAC", "2BAC"}
        if level not in allowed_levels:
            raise ValueError("Invalid level.")

    