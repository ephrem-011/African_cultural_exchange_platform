# Generated by Django 5.1.6 on 2025-03-25 18:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_rename_user_id_event_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='atendee',
            new_name='attendee',
        ),
    ]
