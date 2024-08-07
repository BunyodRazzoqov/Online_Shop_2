# Generated by Django 5.0.7 on 2024-08-07 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0003_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]