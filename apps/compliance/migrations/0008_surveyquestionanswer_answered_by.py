# Generated by Django 2.1.5 on 2019-04-04 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('compliance', '0007_auto_20190403_0347'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyquestionanswer',
            name='answered_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]