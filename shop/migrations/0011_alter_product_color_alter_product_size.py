# Generated by Django 5.0.4 on 2024-05-17 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_userprofile_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(blank=True, null=True, to='shop.color', verbose_name='Ranglar'),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, null=True, to='shop.size', verbose_name='Olchamlar'),
        ),
    ]
