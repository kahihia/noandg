# Generated by Django 2.1.5 on 2019-04-04 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0019_auto_20190403_0302'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='commissioned',
            field=models.BooleanField(default=False),
        ),
    ]
