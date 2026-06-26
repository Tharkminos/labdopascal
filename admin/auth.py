from functools import wraps
from flask import session, abort

def permission_required(*permissions):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for permission in permissions:
                if session.get(permission, False):
                    return func(*args, **kwargs)

            abort(403)

        return wrapper

    return decorator
