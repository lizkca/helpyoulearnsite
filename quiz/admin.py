from django.contrib import admin
from .models import QuizImage, Word

@admin.register(QuizImage)
class QuizImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'description')
    list_filter = ('upload_date',)
    search_fields = ('title', 'description')
    date_hierarchy = 'upload_date'


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'meaning', 'created_at', 'updated_at')
    search_fields = ('word', 'meaning')
    list_filter = ('created_at', 'updated_at')
