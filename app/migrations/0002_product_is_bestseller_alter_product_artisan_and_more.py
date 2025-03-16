# Generated by Django 5.1.6 on 2025-03-16 06:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_fix_admin_log_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_bestseller',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='artisan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.artisan'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('wood-crafts', 'Wood Crafts'), ('pottery', 'Pottery'), ('textiles', 'Textiles'), ('metal-works', 'Metal Works'), ('paper-crafts', 'Paper Crafts'), ('jewelry', 'Jewelry'), ('other', 'Other')], max_length=20),
        ),
    ]
