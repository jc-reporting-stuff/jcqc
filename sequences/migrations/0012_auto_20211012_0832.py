# Generated by Django 3.2.8 on 2021-10-12 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0017_auto_20211004_0743'),
        ('sequences', '0011_alter_sequence_hardcopy'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_id', models.IntegerField()),
                ('status', models.CharField(choices=[('s', 'Submitted'), ('p', 'Preparing'), ('r', 'Running'), ('c', 'Completed')], max_length=1)),
                ('plate_name', models.CharField(blank=True, max_length=20, null=True)),
                ('well', models.CharField(blank=True, max_length=10, null=True)),
                ('submit_date', models.DateField(auto_now_add=True)),
                ('complete_date', models.DateField(blank=True, null=True)),
                ('filename', models.CharField(blank=True, max_length=150, null=True)),
                ('hardcopy', models.BooleanField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
                ('primer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sequences.primer')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(choices=[('no', 'None'), ('gc', 'GC rich'), ('at', 'AT rich'), ('lr', 'Long repeat'), ('hp', 'Homopolymer')], max_length=2)),
                ('type', models.CharField(choices=[('pl', 'Plasmid'), ('pp', 'PCR product'), ('co', 'Cosmid'), ('ot', 'Other')], max_length=2)),
                ('template_size', models.IntegerField()),
                ('insert_size', models.IntegerField(blank=True, null=True)),
                ('pcr_purify', models.BooleanField(verbose_name='PCR Purify?')),
                ('template_concentration', models.IntegerField()),
                ('template_volume', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('primers', models.ManyToManyField(related_name='sequences', through='sequences.Reaction', to='sequences.Primer')),
            ],
        ),
        migrations.DeleteModel(
            name='Sequence',
        ),
        migrations.AddField(
            model_name='reaction',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sequences.template'),
        ),
    ]