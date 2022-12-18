from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, username, email, birth_date, sex, password=None, **extra_fields):
        if not username:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')

        if not birth_date:
            raise ValueError('Дата рождения (YYYY-MM-DD) должна быть установлена')

        if not sex:
            raise ValueError('Ваш гендер (MALE/FEMALE) должен быть установлен')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, birth_date=birth_date, sex=sex, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, birth_date, sex, password=None, **extra_fields):

        extra_fields.setdefault('is_worker', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, birth_date, sex, password, **extra_fields)

    def create_worker(self, username, email, birth_date, sex, password=None, **extra_fields):

        extra_fields.setdefault('is_worker', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_worker') is not True:
            raise ValueError('Исполнитель должен иметь is_worker=True.')

        return self._create_user(username, email, birth_date, sex, password, **extra_fields)

    def create_staff(self, username, email, birth_date, sex, password=None, **extra_fields):

        extra_fields.setdefault('is_worker', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_worker') is not True:
            raise ValueError('Исполнитель должен иметь is_worker=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        return self._create_user(username, email, birth_date, sex, password, **extra_fields)

    def create_superuser(self, username, email, birth_date, sex, password, **extra_fields):

        extra_fields.setdefault('is_worker', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_worker') is not True:
            raise ValueError('Суперпользователь должен иметь is_worker=True.')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(username, email, birth_date, sex, password, **extra_fields)