# Generated by Django 5.1.2 on 2024-10-18 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0003_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='image_file',
        ),
        migrations.AddField(
            model_name='image',
            name='image_url',
            field=models.URLField(default='https://via.placeholder.com/'),
        ),
    ]
