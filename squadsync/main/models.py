from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    interested_sport = models.CharField(max_length=100)
    experience_level = models.CharField(
        max_length=20,
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced')
        ]
    )
    profile_picture = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    extra_photos = models.ManyToManyField('ProfilePhoto', blank=True)

    def __str__(self):
        return self.user.username

class ProfilePhoto(models.Model):
    image = models.ImageField(upload_to='user_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.image)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    rating = models.IntegerField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    

    def __str__(self):
        return f"{self.user.username} - {self.rating}"


class ScheduledMatch(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    sport = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    players_needed = models.IntegerField()
    cash_prize = models.CharField(max_length=50, blank=True, null=True)
    chat_link = models.URLField(max_length=300, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    match_image = models.ImageField(upload_to='match_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ⭐ NEW FIELDS ⭐
    joined_players = models.ManyToManyField(User, related_name='joined_matches', blank=True)

    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')

    RESULT_CHOICES = [
        ('none', 'Not Played'),
        ('win', 'Win'),
        ('loss', 'Loss'),
        ('draw', 'Draw')
    ]
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, default='none')

    notes = models.TextField(blank=True, null=True)   # personal notes

    def __str__(self):
        return self.title


class Note(models.Model):
    COLOR_CHOICES = [
        ("#FFF3B0", "soft-yellow"),
        ("#FFD6E7", "soft-pink"),
        ("#D6F5D6", "soft-green"),
        ("#DCEBFF", "soft-blue"),
        ("#F0E6FF", "soft-purple"),
        ("#FFF0E0", "soft-peach"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    match_name = models.CharField(max_length=150)
    sport = models.CharField(max_length=80)
    date = models.DateField()
    description = models.TextField()
    color = models.CharField(max_length=7, choices=COLOR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.match_name} - {self.user.username}"
