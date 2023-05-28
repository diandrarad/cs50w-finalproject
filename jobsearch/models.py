from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]

    role = models.CharField(max_length=50, choices=USER_ROLE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='profile_picture/')
    # Other fields for user profile (e.g., personal details, resumes, saved job preferences)


class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    industry = models.CharField(max_length=100)
    employee_size = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/')
    # Other fields for company (e.g., contact information)


class JobListing(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    application_instructions = models.TextField()
    salary = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class SavedJob(models.Model):
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE)
    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)


class Application(models.Model):
    job_listing = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    interview_date = models.DateTimeField(null=True, blank=True)
    # Other fields for application


class SavedSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keywords = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=100)
    remote_only = models.BooleanField(default=False)
    # Other fields for saved search


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    # Other fields for resume


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # Other fields for message


# Add additional models and fields as per your project's requirements
