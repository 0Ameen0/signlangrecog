# Generated by Django 5.1.4 on 2025-05-01 06:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signapp', '0011_user_log_is_active_user_log_last_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_date', models.DateField(auto_now_add=True)),
                ('feedback', models.CharField(max_length=500)),
                ('login_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signapp.user_log')),
            ],
        ),
    ]
