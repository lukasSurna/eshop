# Generated by Django 4.2.7 on 2023-11-16 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0002_alter_product_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20, verbose_name='order_number')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('phone', models.CharField(max_length=20, verbose_name='phone')),
                ('email', models.CharField(max_length=50, verbose_name='email')),
                ('address_1', models.CharField(max_length=50, verbose_name='address 1')),
                ('address_2', models.CharField(blank=True, max_length=50, verbose_name='address 2')),
                ('country', models.CharField(max_length=50, verbose_name='country')),
                ('city', models.CharField(max_length=50, verbose_name='city')),
                ('order_comment', models.CharField(max_length=250, verbose_name='order comment')),
                ('order_total', models.FloatField(verbose_name='order total')),
                ('tax', models.FloatField(verbose_name='tax')),
                ('status', models.CharField(choices=[(0, 'New'), (1, 'Accepted'), (2, 'Completed'), (3, 'Cancelled')], default=0, max_length=10, verbose_name='status')),
                ('ip', models.CharField(blank=True, max_length=25, verbose_name='ip')),
                ('is_ordered', models.BooleanField(default=False, verbose_name='is ordered')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100, verbose_name='payment id')),
                ('amount_paid', models.CharField(max_length=100, verbose_name='amount paid')),
                ('status', models.CharField(max_length=100, verbose_name='status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('product_price', models.FloatField(verbose_name='product price')),
                ('ordered', models.BooleanField(default=False, verbose_name='ordered')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='order')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment', verbose_name='payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'orderProduct',
                'verbose_name_plural': 'orderProducts',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment', verbose_name='payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
