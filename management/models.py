from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from AIEP.settings import BASE_DIR
from PIL import Image
from django.forms import ModelChoiceField
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

class TaskColumn(models.Model):
    title = models.CharField(max_length=100, blank=True)

    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

# Create your models here.
class TaskSubmit(models.Model):
    methods = (
        ('算法一', '算法一'),
        ('算法二', '算法二'),
        ('算法三', '算法三'),
    )
    index = (
        ('类型一', '类型一'),
        ('类型二', '类型二'),
    )
    modelTypes = (
        ('类型一', '类型一'),
        ('类型二', '类型二'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    img = models.ImageField(upload_to='%Y%m%d/task', default="static/img/not_login_user.jpg")
    #比赛标题
    title = models.CharField(max_length=20)
    description = models.TextField()
    #浏览量
    total_views = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    #比赛开始时间
    startTime = models.DateTimeField(default=timezone.now)
    #比赛截止时间
    endTime = models.DateTimeField(default=timezone.now)
    #比赛标签
    tags = TaggableManager(blank=True)
    ind = models.CharField(max_length=10, choices=index, help_text='评测指标', default="类型一")
    #攻击算法
    algorithm = models.CharField(max_length=20, choices=methods, default="算法一")
    dataset = models.CharField(max_length=20, default="default")
    #模型格式
    modelType = models.CharField(max_length=20, choices=modelTypes, default="类型一")
    participant = models.ManyToManyField(User)
    submit = models.ManyToManyField('runSubmit')

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
    index = (
        ('类型一', '类型一'),
        ('类型二', '类型二'),
    )
    methods = (
        ('算法一', '算法一'),
        ('算法二', '算法二'),
        ('算法三', '算法三'),
    )
    state = (
        ('评测中', '评测中'),
        ('暂停', '暂停'),
        ('完成', '完成'),
    )
    public = (
        ('公开', '公开'),
        ('私有', '私有'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dataset = models.CharField(max_length=20, default="default")
    created = models.DateTimeField(default=timezone.now)
    algorithm = models.CharField(max_length=10, choices=methods, help_text='攻击算法', default="算法一")
    #评测指标
    ind = models.CharField(max_length=10, choices=index, help_text='评测指标', default="类型一")
    #模型文件
    model = models.FileField(blank=True)
    #模型名称
    modelname = models.CharField(max_length=20, default="default")
    #评测状态
    state = models.CharField(max_length=10, choices=state, default="评测中")
    public = models.CharField(max_length=10, choices=public, default="私有")

class Datasets(models.Model):
    public = (
        ('公开', '公开'),
        ('私有', '私有'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField()
    #规格
    specifications = models.CharField(max_length=10)
    dataType = models.CharField(max_length=10)
    #是否公开
    public = models.CharField(max_length=3, choices=public, default="私有")
    created = models.DateTimeField(default=timezone.now)
    datasets = models.FileField(upload_to='DataSets/')

    def __str__(self):
        return self.name

class Task_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey('TaskSubmit', on_delete=models.CASCADE)
    submitNum = models.PositiveIntegerField(default=0)
    best = models.PositiveIntegerField(default=0)
    bestTime = models.DateTimeField(default=timezone.now)

class Comment(MPTTModel):
    Task = models.ForeignKey(
        TaskSubmit,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    # 新增，mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    # 替换 Meta 为 MPTTMeta
    # class Meta:
    #     ordering = ('created',)
    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]
