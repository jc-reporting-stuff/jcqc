from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_user(self, username, email, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        return self.create_user(username, email, password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('p', 'Supervisor'),
        ('s', 'Student'),
        ('e', 'External')
    )
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    extension = models.CharField(max_length=40, blank=True)
    fax_number = models.CharField(max_length=30, blank=True)
    institution = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=150, blank=True)
    room_number = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=150)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=150)
    create_date = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(
        max_length=1, choices=USER_TYPE, default='s')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    students = models.ManyToManyField(
        'self', related_name="supervisors", symmetrical=False, through='Preapproval')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'display_name']

    objects = CustomAccountManager()

    @property
    def is_external(self):
        return self.user_type == 'e'

    @property
    def is_student(self):
        return self.user_type == 's'

    @property
    def is_supervisor(self):
        return self.user_type == 'p'

    def get_financial_accounts(self):
        if self.is_student:
            return Account.objects.filter(owner__linked_students__student=self, owner__linked_students__approved=True, is_active=True)
        else:
            return Account.objects.filter(owner=self, is_active=True)

    def display_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.username

    @property
    def type(self):
        if self.is_student or self.is_supervisor or self.is_staff or self.is_superuser:
            return 'Internal'
        else:
            return 'External'

# This is a bit confusing since users are also in the accounts folder, I'm sorry.
# This models is definitely the Financial Accounts model.


class Account(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='accounts')
    create_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=50)
    comment = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['owner', '-is_active']

    def __str__(self):
        return self.comment


class Preapproval(models.Model):
    supervisor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='linked_students')
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='linked_supervisors')
    approved = models.BooleanField(default=False)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='account_owner', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def add_new(student, supervisor, account=None, approved=False):
        return Preapproval.objects.create(student=student, supervisor=supervisor, account=account, approved=approved)

    def __str__(self):
        return ' approving '.join([self.supervisor.username, self.student.username])
