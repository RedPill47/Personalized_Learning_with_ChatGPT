# Generated by Django 4.0.10 on 2024-05-25 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_delete_chatmessage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
