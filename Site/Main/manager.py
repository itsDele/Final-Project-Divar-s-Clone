from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import random
import string


class MyUserManager(BaseUserManager):
    def create_normal_user(self, user_name, user_password, **additional_fields):
        if not user_name:
            raise ValueError(_("The username must be provided"))
        new_user = self.model(username=user_name, **additional_fields)
        new_user.set_password(user_password)
        new_user.save()
        return new_user

    def create_admin_user(self, user_name, user_password, **additional_fields):
        additional_fields.setdefault("is_staff", True)
        additional_fields.setdefault("is_superuser", True)
        additional_fields.setdefault("is_active", True)

        if additional_fields.get("is_staff") is not True:
            raise ValueError(_("Admin user must have is_staff=True."))
        if additional_fields.get("is_superuser") is not True:
            raise ValueError(_("Admin user must have is_superuser=True."))
        return self.create_normal_user(user_name, user_password, **additional_fields)

def generate_random_token(length):
    token = "".join(random.choice(string.ascii_letters) for _ in range(length))
    return token