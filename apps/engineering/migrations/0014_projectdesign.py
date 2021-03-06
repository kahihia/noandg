# Generated by Django 2.1.5 on 2019-03-20 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0013_auto_20190320_1920'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectDesign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('document', models.FileField(upload_to='designs')),
                ('design_type', models.CharField(choices=[('FEED', 'FEED'), ('HAZOP', 'HAZOP'), ('MODELING', 'MODELING')], default='FEED', max_length=68)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='engineering.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
