# Generated by Django 4.1.7 on 2023-03-03 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='due_date',
            field=models.DateField(default='03-03-2023'),
        ),
    ]
