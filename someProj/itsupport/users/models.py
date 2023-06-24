from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='user'):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, role='admin'):
        user = self.create_user(username=username, email=email, password=password, role=role)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'admin'),
    )
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')
    role = models.CharField(max_length=10, default='user')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    

class Problem(models.Model):
    PROBLEM_TYPES = (
        ('printer', 'Printer'),
        ('internet', 'Internet'),
        ('pc', 'PC'),
        ('other', 'Other'),
    )

    problem_description = models.CharField(max_length=255)
    problem_type = models.CharField(max_length=20, choices=PROBLEM_TYPES)
    floor = models.PositiveSmallIntegerField(choices=((1, 'First floor'), (2, 'Second floor')))
    room_number = models.CharField(max_length=20)
    problem_solved=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.problem_type} in room {self.room_number}'
    
class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='comments')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
    

class Report(models.Model):
    STATUS_CHOICES = (
        ('resolved', 'Resolved'),
        ('in_progress', 'In Progress'),
        ('not_resolved', 'Not Resolved'),
    )

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, default=1)
    solution = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    solver = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=1)
    notes = models.TextField()