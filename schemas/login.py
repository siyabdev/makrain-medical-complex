#Login request
class LoginRequest:
    def __init__(self, data):
        self.username = data.get("username")
        self.password = data.get("password")
    
    def is_valid(self):
        #Fields required
        if not self.username:
            return False, "Employee username required for login."
        
        if not self.password:
            return False, "Employee password required for login."
        
        #Fields validation
        if len(self.username) < 6:
            return False, "Employee username must be at least 6 characters long."

        if len(self.password) < 6:
            return False, "Employee password must be at least 6 characters long."
        
        return True, None

#Login response
class LoginResponse:
    def __init__(self, token, employee_id, username, is_active):
        self.token = token
        self.employee_id = employee_id
        self.username = username
        self.is_active = is_active
    
    def to_dict(self):
        return {
            "token": self.token,
            "employee_id": self.employee_id,
            "username": self.username,
            "is_active": self.is_active
        }