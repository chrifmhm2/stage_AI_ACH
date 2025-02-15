# Generated by Django 5.0.7 on 2024-08-16 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_acnt_num', models.CharField(default='default_old_acnt_num', max_length=100)),
                ('acnt_num', models.CharField(default='default_acnt_num', max_length=100)),
                ('account_name', models.CharField(default='default_account_name', max_length=255)),
                ('curr', models.CharField(default='MRU', max_length=3)),
                ('old_rib', models.CharField(default='default_old_rib', max_length=100)),
                ('new_rib', models.CharField(default='default_new_rib', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('bank_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('bank_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MsgIDSeq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_id_seq', models.IntegerField()),
            ],
        ),
    ]
