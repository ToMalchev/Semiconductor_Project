# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 04:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uploading_data', '0002_auto_20170719_2320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xml_intensities',
            name='ext_training',
        ),
        migrations.AddField(
            model_name='upload',
            name='ext_training',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to='uploading_data.training'),
        ),
    ]