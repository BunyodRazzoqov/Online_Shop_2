# Generated by Django 5.0.7 on 2024-08-07 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='Categories',
        ),
        migrations.AlterModelTable(
            name='comment',
            table='Comments',
        ),
        migrations.AlterModelTable(
            name='order',
            table='Orders',
        ),
        migrations.AlterModelTable(
            name='product',
            table='Products',
        ),
    ]
