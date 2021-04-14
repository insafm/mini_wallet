# Generated by Django 2.2.8 on 2021-04-13 10:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ins_user', '0007_profile_user_xid'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=15, max_digits=50)),
                ('balance', models.DecimalField(decimal_places=15, max_digits=50)),
                ('category', models.CharField(max_length=100)),
                ('notes', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('credit_status', models.SmallIntegerField(blank=True, default=0)),
                ('reference_id', models.CharField(blank=True, max_length=255)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('associated_user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='associated_user', to='ins_user.Profile')),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='ins_user.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='MasterWallet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('enabled_at', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('balance', models.DecimalField(decimal_places=15, max_digits=50)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='ins_user.Profile')),
            ],
        ),
        migrations.AddIndex(
            model_name='wallettransaction',
            index=models.Index(fields=['user'], name='mini_wallet_user_id_c08266_idx'),
        ),
        migrations.AddIndex(
            model_name='masterwallet',
            index=models.Index(fields=['user'], name='mini_wallet_user_id_a0dd12_idx'),
        ),
        migrations.AlterIndexTogether(
            name='masterwallet',
            index_together={('user', 'balance')},
        ),
    ]