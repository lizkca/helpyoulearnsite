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
from django.contrib.auth.decorators import login_required
from .models import ImageDescription

def index(request):
    all_images = QuizImage.objects.all()
    random_image = random.choice(all_images) if all_images else None
    user_description = None
    if random_image and request.user.is_authenticated:
        user_description = ImageDescription.objects.filter(
            image=random_image,
            user=request.user
        ).first()
    return render(request, 'quiz/index.html', {
        'random_image': random_image,
        'user_description': user_description
    })

@login_required
def save_description(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(QuizImage, id=image_id)
        description = request.POST.get('description')
        if description:
            # 获取或创建用户的描述
            obj, created = ImageDescription.objects.update_or_create(
                image=image,
                user=request.user,
                defaults={'description': description}
            )
            messages.success(request, '描述保存成功！')
    return redirect('quiz:index')

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功！')
            return redirect('quiz:index')
    else:
        form = UserCreationForm()
    return render(request, 'quiz/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '登录成功！')
                return redirect('quiz:index')
    else:
        form = AuthenticationForm()
    return render(request, 'quiz/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, '已成功退出！')
    return redirect('quiz:index')

from django.contrib.auth.decorators import login_required

@login_required
def my_descriptions(request):
    user_descriptions = ImageDescription.objects.filter(user=request.user).select_related('image')
    return render(request, 'quiz/my_descriptions.html', {
        'descriptions': user_descriptions
    })


def learn_with_images(request):
    all_images = QuizImage.objects.all()
    random_image = random.choice(all_images) if all_images else None
    return render(request, 'quiz/learn_with_images.html', {
        'random_image': random_image
    })

from django.shortcuts import render
from .models import QuizImage, Word  # Add Word to the imports

def practice_pronunciation(request):
    words = Word.objects.all().order_by('?')[:3]  # Get 3 random words
    return render(request, 'quiz/practice_pronunciation.html', {
        'words': words
    })

