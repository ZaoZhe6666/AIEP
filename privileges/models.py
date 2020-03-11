from django.db import models

# Create your models here.
from django.contrib.auth.models import User

import os
import uuid
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    # 模型类中设置:blank=True,表示代码中创建数据库记录时该字段可传空白(空串,空字符串)
    org = models.CharField('Organization', max_length=128, blank=True)
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)
    mod_data = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'User profile'

    def __str__(self):
        # return self.user.__str__()
        return "{}".format(self.user.__str__())

    def save_avatar(self, upload_image, username):
        # 创建与用户名的文件夹
        upload_path = settings.MEDIA_ROOT+'\\avatar\\'+username
        try:
            os.makedirs(upload_path)
        except:
            pass
        # 生成一个随机字符串
        uuid_str_name = uuid.uuid4().hex + '.jpg'
        # 保存
        with open(os.path.join(upload_path, uuid_str_name), 'wb+') as file:
            for chunk in upload_image.chunks():
                file.write(chunk)
        return uuid_str_name