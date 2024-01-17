# Generated by Django 5.0.1 on 2024-01-15 05:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('product_location', models.CharField(choices=[('private_box', 'Private Box'), ('medicare', 'Medicare'), ('food', 'Food')], default='medicare', max_length=15)),
                ('product_price', models.DecimalField(blank=True, decimal_places=4, default=0.0, max_digits=5, null=True)),
                ('product_vat', models.DecimalField(blank=True, decimal_places=4, default=0.0, max_digits=5, null=True)),
                ('product_discount', models.DecimalField(blank=True, decimal_places=4, default=0.0, max_digits=5, null=True)),
                ('product_barcode', models.CharField(max_length=50, unique=True)),
                ('product_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='file_upload.category')),
            ],
        ),
    ]