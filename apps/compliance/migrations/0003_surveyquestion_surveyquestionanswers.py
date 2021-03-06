# Generated by Django 2.1.5 on 2019-03-23 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compliance', '0002_auto_20190323_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('question_type', models.CharField(choices=[('Shipping', 'Shipping'), ('Fabrication', 'Fabrication')], default='Shipping', max_length=68)),
                ('status', models.BooleanField(default=False)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['question'],
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestionAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compliance.SurveyQuestion')),
            ],
            options={
                'ordering': ['question'],
            },
        ),
    ]
