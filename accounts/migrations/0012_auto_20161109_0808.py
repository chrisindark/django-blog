# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_userfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='./images'),
        ),
    ]
