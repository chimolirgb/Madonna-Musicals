# Generated by Django 3.2.5 on 2021-07-28 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicals', '0003_auto_20210728_1158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='photo',
            new_name='music',
        ),
    ]