from functools import wraps
from .models import AuthUser, AuthToken
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)


def login_required():

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = AuthToken.objects.verify(request.headers['Authorization'])
            if token is None:
                return Response({}, status=HTTP_400_BAD_REQUEST)
            request.session['user_id'] = token.user.id
            request.session['user_token'] = token.code
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
