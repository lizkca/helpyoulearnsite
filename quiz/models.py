from django.db import models

class QuizImage(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    image = models.ImageField(upload_to='quiz_images/%Y/%m/%d/', verbose_name='图片')
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    description = models.TextField(blank=True, verbose_name='描述')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']
