# Generated by Django 4.2 on 2023-05-17 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_testmodel_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testmodel',
            name='photo',
        ),
        migrations.AddField(
            model_name='task',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/'),
        ),
    ]