# Generated by Django 2.2.3 on 2019-08-25 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_todo_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
