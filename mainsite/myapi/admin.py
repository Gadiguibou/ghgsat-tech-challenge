from django.contrib import admin
from .models import Observation, Target

admin.site.register(Target)
admin.site.register(Observation)
