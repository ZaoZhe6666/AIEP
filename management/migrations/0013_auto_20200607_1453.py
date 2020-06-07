# Generated by Django 2.2.3 on 2020-06-07 06:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_auto_20200607_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='runsubmit',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='runsubmit',
            name='modelname',
            field=models.CharField(default='default', max_length=20),
        ),
        migrations.AddField(
            model_name='runsubmit',
            name='public',
            field=models.CharField(choices=[('公开', '公开'), ('私有', '私有')], default='私有', max_length=10),
        ),
        migrations.AddField(
            model_name='runsubmit',
            name='state',
            field=models.CharField(choices=[('评测中', '评测中'), ('暂停', '暂停'), ('完成', '完成')], default='评测中', max_length=10),
        ),
    ]
