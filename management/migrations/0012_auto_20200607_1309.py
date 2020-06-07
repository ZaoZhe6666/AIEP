# Generated by Django 2.2.3 on 2020-06-07 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_forum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attack_method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attack_method', models.CharField(default='default', max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='runsubmit',
            name='algorithm',
        ),
        migrations.RemoveField(
            model_name='runsubmit',
            name='created',
        ),
        migrations.RemoveField(
            model_name='runsubmit',
            name='ind',
        ),
        migrations.RemoveField(
            model_name='runsubmit',
            name='modelname',
        ),
        migrations.RemoveField(
            model_name='runsubmit',
            name='public',
        ),
        migrations.RemoveField(
            model_name='runsubmit',
            name='state',
        ),
        migrations.AddField(
            model_name='runsubmit',
            name='description',
            field=models.CharField(default='default', max_length=300),
        ),
        migrations.AddField(
            model_name='runsubmit',
            name='evaluate_method',
            field=models.CharField(default='default', max_length=20),
        ),
        migrations.AddField(
            model_name='runsubmit',
            name='model_data',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='runsubmit',
            name='time_part',
            field=models.CharField(default='default', max_length=30),
        ),
        migrations.AddField(
            model_name='runsubmit',
            name='title',
            field=models.CharField(default='default', max_length=20),
        ),
        migrations.AddField(
            model_name='runsubmit',
            name='attack_method',
            field=models.ManyToManyField(to='management.Attack_method'),
        ),
    ]
