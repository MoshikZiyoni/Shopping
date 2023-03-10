# Generated by Django 3.2.16 on 2023-02-13 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20230204_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.SmallIntegerField(max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.SmallIntegerField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.SmallIntegerField(max_length=10),
        ),
    ]
