# Generated by Django 5.0.3 on 2024-04-06 13:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storys', '0004_author_is_premium'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_img',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='stories/category/'),
            preserve_default=False,
        ),
    ]