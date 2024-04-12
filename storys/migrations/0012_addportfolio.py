# Generated by Django 5.0.3 on 2024-04-12 11:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storys', '0011_alter_story_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddPortfolio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('portfolio', models.CharField(choices=[('Medium', 'Medium'), ('Webite', 'Website'), ('Other', 'Other'), ('social', 'Social Media')], max_length=100)),
                ('link', models.URLField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to='storys.author')),
            ],
        ),
    ]
