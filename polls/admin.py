"""
Register your models here

Herein models are registered with Django admin so that the Admin page can be used to edit them.
"""
from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.StackedInline):
    # Stacked FK subinterface, default 3
    model = Choice
    extra = 3

class ChoiceInline(admin.TabularInline):
    # Tabular FK subinterface, default 3
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    # Group fields in sets
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    # Change the list display (attributes and methods are possible)
    list_display = ["question_text", "pub_date", "was_published_recently"]
    # Adds a filter sidebar
    list_filter = ["pub_date"]
    # Add search functionality
    search_fields = ["question_text"]

admin.site.register(Question, QuestionAdmin)

#admin.site.register(Question) # 🌳 Tell Django that Question has an Admin Interface