# Generated by Django 3.2.9 on 2021-11-11 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('UAH', 'UAH')], default='USD', max_length=5),
        ),
    ]