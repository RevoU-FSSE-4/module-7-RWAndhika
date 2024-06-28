from functools import wraps
from flask_login import current_user

def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and role == 'Admin' and current_user.role == 'Admin':
                return func(*args, **kwargs)
            elif current_user.is_authenticated and role == 'User' and current_user.role == 'Admin':
                return func(*args, **kwargs)
            elif current_user.is_authenticated and role == 'User' and current_user.role == 'User':
                return func(*args, **kwargs)
            else:
                return {"message": "Unauthorized"}, 403
        return wrapper
    
    return decorator