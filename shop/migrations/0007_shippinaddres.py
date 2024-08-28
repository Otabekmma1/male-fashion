# Generated by Django 5.0.4 on 2024-05-17 01:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippinAddres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=14)),
                ('email', models.EmailField(max_length=100)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.customer')),
            ],
        ),
    ]
