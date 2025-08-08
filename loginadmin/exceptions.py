from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated):
        if response is not None:
            response.data = {'message': 'Please login before updating your profile.'}
    elif isinstance(exc, PermissionDenied):
        if response is not None:
            response.data = {'message': 'Please log in to add your details.'}

    return response
