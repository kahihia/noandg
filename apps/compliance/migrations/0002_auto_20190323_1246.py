# Generated by Django 2.1.5 on 2019-03-23 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compliance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engineering.Project'),
        ),
    ]
