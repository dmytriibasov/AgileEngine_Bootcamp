# Generated by Django 3.2.9 on 2021-11-19 15:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_rename_receiver_transaction_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='contact',
            new_name='email',
        ),
    ]
