# Generated by Django 3.2.7 on 2021-09-28 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210928_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='extension',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='user',
            name='fax_number',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
