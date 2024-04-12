# Generated by Django 5.0.3 on 2024-04-05 07:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=12)),
                ('profile', models.ImageField(upload_to='stories/author/images/')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('bio', models.TextField()),
                ('pen_name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('audience', models.CharField(choices=[('Everyone', 'Everyone'), ('Teen', 'Teens'), ('Adults', 'Adults'), ('Children', 'Children')], max_length=10)),
                ('language', models.CharField(choices=[('English', 'English'), ('Hindi', 'Hindi'), ('Marathi', 'Marathi'), ('Telugu', 'Telugu'), ('Tamil', 'Tamil'), ('Kannada', 'Kannada'), ('Bengali', 'Bengali'), ('Gujarati', 'Gujarati'), ('Odia', 'Odia'), ('Punjabi', 'Punjabi'), ('Malayalam', 'Malayalam')], max_length=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='stories/story/images/')),
                ('tag', models.CharField(max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storys.author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storys.category')),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('part_image', models.ImageField(upload_to='stories/part/images/')),
                ('part_number', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='storys.story')),
            ],
        ),
    ]