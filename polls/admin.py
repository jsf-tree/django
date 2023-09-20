"""
Register your models here

Herein models are registered with Django admin so that the Admin page can be used to edit them.
"""
from django.contrib import admin
from .models import Question, Choice # 🌳 

admin.site.register(Choice)
admin.site.register(Question) # 🌳 Tell django that Question has an Admin Interface