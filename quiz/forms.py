from django import forms
from .models import QuizImage

class QuizImageForm(forms.ModelForm):
    class Meta:
        model = QuizImage
        fields = ['title', 'image', 'description']