# Generated by Django 2.1.5 on 2019-03-22 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0016_auto_20190322_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='logistics_bidding',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
