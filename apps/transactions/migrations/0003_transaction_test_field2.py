# Generated by Django 3.2.9 on 2021-11-11 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transaction_test_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='test_field2',
            field=models.IntegerField(null=True),
        ),
    ]
