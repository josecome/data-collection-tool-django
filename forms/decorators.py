from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .models import Project_Form_Meta, Project_Form

def is_admin(user):
    return User.objects.filter(is_superuser=1).exists()

admin_required = user_passes_test(is_admin)


def user_is_project_author(function):
    def wrap(request, *args, **kwargs):
        entry = Project_Form.objects.get(pk=kwargs['user_id'])
        if entry.created_by == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap