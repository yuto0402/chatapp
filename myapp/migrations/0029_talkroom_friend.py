# Generated by Django 5.1 on 2024-09-24 02:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_remove_friend_registrationdate_friend_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='talkroom',
            name='friend',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.friend'),
        ),
    ]
