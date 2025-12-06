from django.contrib import admin
from .models import Profile, Feedback,ScheduledMatch

admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(ScheduledMatch)