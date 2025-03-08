from rest_framework.permissions import BasePermission
from users.thread_local import set_current_user
from users.models import User

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        user_id = request.COOKIES.get("uid")
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                set_current_user(user)  # Store user in thread-local
                return True
            except User.DoesNotExist:
                return False
        return False
