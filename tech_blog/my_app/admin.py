from django.contrib import admin
from .models import Blog, Comment
from mediumeditor.admin import MediumEditorAdmin

# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)