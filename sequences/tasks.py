from __future__ import absolute_import, unicode_literals
import os

from celery import shared_task
from django.conf import settings

from django.utils import timezone
from datetime import timedelta
import time

from accounts.models import User


@shared_task(name='inactivate_dormant_users')
def inactivate_dormant_users(weeks):
    inactivation_time = timezone.now() - timedelta(weeks=weeks)
    users = User.objects.filter(last_login__lte=inactivation_time)
    for user in users:
        user.is_active = False
        user.save()
    return [user.username for user in users]


@shared_task(name='delete_old_sequences')
def remove_old(days=14):
    # Date measured in epoch time
    inactivation_time = float((
        timezone.now() - timedelta(days=days)).strftime('%s'))
    user_sequence_folders = os.path.join(
        settings.FILES_BASE_DIR, settings.CUSTOMER_SEQUENCES_DIR)
    files_list = []
    for folder_name, subfolders, filenames in os.walk(user_sequence_folders):
        for file in filenames:
            files_list.append(os.path.join(folder_name, file))

    for file in files_list:
        # File modified date in epoch time
        file_modified_date = os.path.getmtime(file)
        if file_modified_date < inactivation_time:
            os.remove(file)
