# Generated by Django 5.0.3 on 2024-04-06 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storys', '0005_category_cat_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='cat_img',
        ),
    ]