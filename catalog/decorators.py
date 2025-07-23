from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def multiple_permissions_required(*perms):
    """
    Decorator check permission
    """
    def check_perms(user):
        if user.is_authenticated and user.has_perms(perms):
            return True

        return False
    
    return user_passes_test(check_perms)