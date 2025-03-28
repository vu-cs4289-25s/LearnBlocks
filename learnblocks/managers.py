from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as get_text_lazy
from .enums import enums


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager.
    """

    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username email and password.
        """
        if not username:
            raise ValueError(get_text_lazy("The Username must be set"))
        if not email:
            raise ValueError(get_text_lazy("The Email must be set"))
        if not password:
            raise ValueError(get_text_lazy("The Password must be set"))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given username, email and password.
        """
        if not username:
            raise ValueError(get_text_lazy("The Username must be set"))
        if not email:
            raise ValueError(get_text_lazy("The Email must be set"))
        if not password:
            raise ValueError(get_text_lazy("The Password must be set"))

        extra_fields.setdefault("role", enums.UserRole.ADMIN)

        if extra_fields.get("role") is not enums.UserRole.ADMIN:
            raise ValueError(get_text_lazy("superuser must have Admin role"))
        return self.create_user(username, email, password, **extra_fields)
