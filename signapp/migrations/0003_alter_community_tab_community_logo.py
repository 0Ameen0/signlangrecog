# Generated by Django 5.1.4 on 2025-02-07 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signapp', '0002_community_tab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community_tab',
            name='community_logo',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
