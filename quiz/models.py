from django.db import models
from django.contrib.auth.models import User

class QuizImage(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    image = models.ImageField(upload_to='quiz_images/%Y/%m/%d/', verbose_name='图片')
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    description = models.TextField(blank=True, verbose_name='描述')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']


class ImageDescription(models.Model):
    image = models.ForeignKey(QuizImage, on_delete=models.CASCADE, related_name='descriptions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class Word(models.Model):
    word = models.CharField(max_length=100, unique=True, verbose_name='单词')
    meaning = models.CharField(max_length=255, verbose_name='含义')
    example = models.TextField(blank=True, verbose_name='例句')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '单词'
        verbose_name_plural = '单词'
        ordering = ['word']

    def __str__(self):
        return self.word
