# Generated by Django 5.0.6 on 2024-07-06 04:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.category'),
        ),
    ]