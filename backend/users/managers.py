from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_superuser(
            self, email, username, first_name, last_name,
            password, **other_fields
    ):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if not other_fields.get('is_staff'):
            raise ValueError('Отказано в доступе')

        if not other_fields.get('is_superuser'):
            raise ValueError('Отказано в доступе')

        return self.create_user(
            email, username, first_name, last_name,
            password=password, **other_fields
        )

    def create_user(self, first_name, last_name,
                    email, password, **other_fields):

        if not email:
            raise ValueError('Укажите email!')

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name,
            last_name=last_name, **other_fields
        )

        user.set_password(password)
        user.save()

        return user
