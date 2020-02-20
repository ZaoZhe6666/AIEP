from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from PIL import Image


class TaskColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)

    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

# Create your models here.
class TaskSubmit(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    img = models.ImageField(upload_to='%Y%m%d/task', blank=True)

    #比赛标题
    title = models.CharField(max_length=20)

    #比赛要求
    description = models.TextField()

    #浏览量
    total_views = models.PositiveIntegerField(default=0)

    #比赛创建时间
    created = models.DateTimeField(default=timezone.now)

    #比赛类别
    category = models.CharField(max_length=20, default="Img")

    #数据集
    dataset = models.FileField(upload_to='%Y%m%d/DataSets/',
                               verbose_name=u'任务数据集',
                               null=True,
                               blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    #获取任务地址
    def get_absolute_url(self):
        return reverse('management:task_detail', args=[self.id])

    #保存时处理照片
    def save(self, *args, **kwargs):
        task = super(TaskSubmit, self).save(*args, **kwargs)

        if self.img and not kwargs.get('update_fields'):
            image = Image.open(self.img)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.img.path)

        return task

    def created_recently(self):
        diff = timezone.now() - self.created

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            return True
        else:
            return False

#图片类，用于存储图片路径
class ShowImgAfterUpload(models.Model):
    file_Path=models.CharField(max_length=32)

class runSubmit(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    image = (
        ('One', 'One'),
        ('Two', 'Two'),
        ('Three', 'Three'),
    )

    gpu = (
        ('gtx1080ti', 'gtx1080ti'),
        ('Two', 'Two'),
        ('Three', 'Three'),
    )

    datasets = (
        ('cifar-20', 'cifar-20'),
        ('cifar-100', 'cifar-100'),
    )

    index = (
        ('套餐一', '套餐一'),
        ('套餐二', '套餐二'),
    )

    # 运行标题
    title = models.CharField(max_length=20)

    img = models.CharField(max_length=10, choices=image, help_text='镜像信息')

    gpu = models.CharField(max_length=10, choices=gpu, help_text='gpu使用')

    retrycount = models.CharField(max_length=10)

    # 项目简介
    description = models.TextField()

    #选择数据集
    dataset = models.CharField(max_length=10, choices=datasets, help_text='数据集选择')

    # 任务提交时间
    created = models.DateTimeField(default=timezone.now)

    # 评测指标
    ind = models.CharField(max_length=10, choices=index, help_text='评测指标')

    #模型文件
    model = models.FileField(upload_to='%Y%m%d/Models')

