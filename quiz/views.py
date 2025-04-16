from django.shortcuts import render, redirect
from .models import QuizImage
from .forms import QuizImageForm

def image_list(request):
    images = QuizImage.objects.all()
    return render(request, 'quiz/image_list.html', {'images': images})

def upload_image(request):
    if request.method == 'POST':
        form = QuizImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('quiz:image_list')
    else:
        form = QuizImageForm()
    return render(request, 'quiz/upload_image.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import QuizImage
import random

def index(request):
    all_images = QuizImage.objects.all()
    random_image = random.choice(all_images) if all_images else None
    return render(request, 'quiz/index.html', {
        'random_image': random_image
    })

def save_description(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(QuizImage, id=image_id)
        description = request.POST.get('description')
        if description:
            image.description = description
            image.save()
            messages.success(request, '描述保存成功！')
    return redirect('quiz:index')

