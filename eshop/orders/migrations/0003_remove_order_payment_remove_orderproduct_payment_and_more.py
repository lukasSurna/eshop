# Generated by Django 4.2.7 on 2023-11-16 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_zip_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='payment',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
