# Generated by Django 2.1.5 on 2019-02-20 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('engineering', '0003_projectequipment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('unit_cost', models.FloatField()),
                ('unit_cost_in', models.CharField(max_length=55)),
                ('description', models.TextField()),
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