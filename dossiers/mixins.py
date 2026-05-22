from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import AccessMixin

class AvocatRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role != 'Avocat':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)