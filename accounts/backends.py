from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User= get_user_model()

class Backend_Perso(ModelBackend):
    def authenticate(self, request, username, passwords, email, **kwargs):
        if username is None or email is None:
            return None
        try:
            user= User.objects.get(username= username, email= email)

        except User.DoesNotExist:
            return None
        if user.check_password(passwords) and self.user_can_authenticate(user):
            return user
                
