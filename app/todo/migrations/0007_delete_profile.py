# Generated by Django 4.1.7 on 2023-02-24 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_profile_remove_todolist_host_delete_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
