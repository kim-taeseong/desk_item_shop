from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CommunityCategory)
admin.site.register(Community)
admin.site.register(CommunityComment)
