# Generated by Django 4.2.7 on 2023-11-16 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='zip_code',
            field=models.CharField(default=0, max_length=15, verbose_name='zip code'),
        ),
    ]