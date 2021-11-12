# Generated by Django 3.2.8 on 2021-11-11 13:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sequences', '0028_worksheet_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worksheet',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='plate',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
