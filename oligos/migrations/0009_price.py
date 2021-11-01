# Generated by Django 3.2.8 on 2021-10-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oligos', '0008_auto_20211006_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scale_40_base', models.DecimalField(decimal_places=2, max_digits=5)),
                ('scale_200_base', models.DecimalField(decimal_places=2, max_digits=5)),
                ('scale_1000_base', models.DecimalField(decimal_places=2, max_digits=5)),
                ('degenerate_40_base', models.DecimalField(decimal_places=2, max_digits=5)),
                ('degenerate_200_base', models.DecimalField(decimal_places=2, max_digits=5)),
                ('degenerate_1000_base', models.DecimalField(decimal_places=2, max_digits=5)),
                ('desalt_fee', models.DecimalField(decimal_places=2, max_digits=5)),
                ('cartridge_fee', models.DecimalField(decimal_places=2, max_digits=5)),
                ('setup_fee', models.DecimalField(decimal_places=2, max_digits=5)),
                ('current', models.BooleanField()),
            ],
        ),
    ]