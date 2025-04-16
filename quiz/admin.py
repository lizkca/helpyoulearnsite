from django.contrib import admin
from .models import QuizImage

@admin.register(QuizImage)
class QuizImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date', 'description')
    list_filter = ('upload_date',)
    search_fields = ('title', 'description')
    date_hierarchy = 'upload_date'
