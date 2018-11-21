from django.contrib import admin

# Register your models here.
from .models import Account
from .models import Course
from .models import Section

admin.site.register(Account)
admin.site.register(Course)
admin.site.register(Section)
