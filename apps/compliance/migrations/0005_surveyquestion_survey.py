# Generated by Django 2.1.5 on 2019-03-23 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compliance', '0004_auto_20190323_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveyquestion',
            name='survey',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='compliance.Survey'),
            preserve_default=False,
        ),
    ]
