from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending',
    )

    def __str__(self):
        return f"{self.full_name} - {self.department} ({self.preferred_date})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} from {self.name}"


class CareerApplication(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    position = models.CharField(max_length=150)
    years_experience = models.CharField(max_length=50)
    resume_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('received', 'Received'),
            ('reviewing', 'Reviewing'),
            ('shortlisted', 'Shortlisted'),
            ('rejected', 'Rejected'),
        ],
        default='received',
    )

    def __str__(self):
        return f"{self.full_name} - {self.position}"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('Female', 'Female'), ('Male', 'Male'), ('Other', 'Other')],
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ChatLog(models.Model):
    session_id = models.CharField(max_length=64, blank=True)
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id} @ {self.created_at}"
