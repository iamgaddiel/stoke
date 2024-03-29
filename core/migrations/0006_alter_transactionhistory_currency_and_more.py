# Generated by Django 5.0 on 2023-12-27 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_userwallet_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionhistory',
            name='currency',
            field=models.CharField(choices=[('btc', 'btc'), ('ltc', 'ltc'), ('eth', 'eth')], default='btc', max_length=200),
        ),
        migrations.AlterField(
            model_name='userwallet',
            name='currency',
            field=models.CharField(choices=[('btc', 'btc'), ('ltc', 'ltc'), ('eth', 'eth')], default='btc', max_length=200),
        ),
    ]
