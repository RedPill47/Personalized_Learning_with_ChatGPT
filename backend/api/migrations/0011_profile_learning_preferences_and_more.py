# Generated by Django 4.0.10 on 2024-05-14 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='learning_preferences',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='learning_preferences',
            field=models.TextField(blank=True, null=True),
        ),
    ]
