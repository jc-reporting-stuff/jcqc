# Generated by Django 3.2.8 on 2021-10-20 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sequences', '0021_reaction_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reaction',
            name='sequence_id',
        ),
    ]
