# Generated by Django 4.1.7 on 2023-02-25 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0012_alter_todolist_options_todolist_updated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='is_done',
            field=models.BooleanField(default=False),
        ),
    ]