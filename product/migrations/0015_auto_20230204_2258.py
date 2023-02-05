# Generated by Django 3.2.16 on 2023-02-04 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_auto_20230204_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='products',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.products'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='quantity',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]