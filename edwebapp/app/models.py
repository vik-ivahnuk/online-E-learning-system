import string

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
import secrets


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user_with_name(self, email, username, full_name, password=None, **extra_fields):
        extra_fields.setdefault('first_name', '')
        extra_fields.setdefault('last_name', '')
        first_name, last_name = full_name.split(' ', 1)
        extra_fields['first_name'] = first_name
        extra_fields['last_name'] = last_name
        return self.create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    backend = 'app.backends.UserBackend'

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


def generate_code():
    allowed_chars = string.digits + string.ascii_lowercase
    code = ''.join(secrets.choice(allowed_chars) for _ in range(8))
    while Course.objects.filter(code=code).exists():
        code = ''.join(secrets.choice(allowed_chars) for _ in range(8))
    return code


class Course(models.Model):
    code = models.CharField(max_length=8, unique=True, default=generate_code)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('course_editor', kwargs={'code': self.code})


class Student(models.Model):
    joined_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='active')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f'{self.user.username} in {self.course.name}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.joined_at = timezone.now()
        super().save(*args, **kwargs)


def generate_code2():
    allowed_chars = string.digits + string.ascii_lowercase
    code = ''.join(secrets.choice(allowed_chars) for _ in range(16))
    while TestModel.objects.filter(code=code).exists():
        code = ''.join(secrets.choice(allowed_chars) for _ in range(16))
    return code


class TestModel(models.Model):
    code = models.CharField(max_length=16, unique=True, default=generate_code2)
    name = models.CharField(max_length=255)
    deadline = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('test_editor', kwargs={'code': self.code})


class Task(models.Model):
    question = models.CharField(max_length=255)
    points = models.FloatField(default=1)
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE)


class Answer(models.Model):
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TestStudent(models.Model):
    scores = models.IntegerField()
    total_score = models.IntegerField(default=0)
    # submitted_on_time = models.BooleanField()
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(TestModel, on_delete=models.CASCADE)


class AnswerStudent(models.Model):
    is_correct = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
