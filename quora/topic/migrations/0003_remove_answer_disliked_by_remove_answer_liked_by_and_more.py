# Generated by Django 4.2.13 on 2024-06-04 07:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topic', '0002_remove_question_title_question_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='disliked_by',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='liked_by',
        ),
        migrations.RemoveField(
            model_name='question',
            name='disliked_by',
        ),
        migrations.RemoveField(
            model_name='question',
            name='liked_by',
        ),
        migrations.AddField(
            model_name='answer',
            name='disliked_by',
            field=models.ManyToManyField(related_name='ans_disliked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='liked_by',
            field=models.ManyToManyField(related_name='ans_liked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='disliked_by',
            field=models.ManyToManyField(related_name='qs_disliked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='liked_by',
            field=models.ManyToManyField(related_name='qs_liked_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
