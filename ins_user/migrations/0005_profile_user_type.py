# Generated by Django 2.2.8 on 2021-02-20 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ins_user', '0004_auto_20200719_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_type',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
