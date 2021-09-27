from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomAccountManager(BaseUserManager):
    def create_user(self, username, email, display_name, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, display_name=display_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, username, email, display_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        return self.create_user(username, email, display_name, password, **other_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150)
    create_date = models.DateTimeField(auto_now_add=True)
    institution = models.CharField(max_length=150)
    is_student = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    students = models.ManyToManyField('self', related_name="supervisors", symmetrical=False, through='Preapproval')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'display_name']

    objects = CustomAccountManager()

    def __str__(self):
        return self.username

class Preapproval(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_student')
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approved_supervisor')
    approved = models.BooleanField(default=False)
    # add accounts to this at some point after model exists