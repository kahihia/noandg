# Generated by Django 2.1.5 on 2019-04-29 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0022_auto_20190429_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdesign',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]