# Generated by Django 4.1.7 on 2023-02-25 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0011_alter_todolist_due_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.AddField(
            model_name='todolist',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]