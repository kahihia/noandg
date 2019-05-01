# Generated by Django 2.1.5 on 2019-04-02 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='civil',
            name='cleared_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cleared_by', to=settings.AUTH_USER_MODEL),
        ),
    ]