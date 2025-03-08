from django.utils.deprecation import MiddlewareMixin
from users.thread_local import set_current_user
from users.models import User

class StoreUserMiddleware(MiddlewareMixin):
    """ Middleware to store user from cookies in thread-local storage """

    def process_request(self, request):
        user_id = request.COOKIES.get("uid")  # Fetch user ID from cookies
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                set_current_user(user)  # Store user in thread-local
            except User.DoesNotExist:
                set_current_user(None)  # If user not found, set None
