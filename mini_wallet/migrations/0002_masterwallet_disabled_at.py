# Generated by Django 2.2.8 on 2021-04-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterwallet',
            name='disabled_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]