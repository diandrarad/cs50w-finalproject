from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Profile(models.Model):
    USER_ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]

    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='profile_picture/')


class SavedJob(models.Model):
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.CharField(max_length=100, default='Default ID')
    category = models.CharField(max_length=100, default='Unknown')
    title = models.CharField(max_length=100, default='')
    salary_max = models.CharField(max_length=100, default='')
    company = models.CharField(max_length=100, default='Undefined')
    location = models.CharField(max_length=100, default='')
    description = models.TextField()
    redirect_url = models.URLField()
    saved_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company}"


class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keywords = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=100)
    remote_only = models.BooleanField(default=False)


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')