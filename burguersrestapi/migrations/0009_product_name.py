# Generated by Django 5.0.4 on 2024-05-25 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('burguersrestapi', '0008_remove_order_hour_order_orderdayhour_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(choices=[('D', 'Drink'), ('B', 'Burguer')], default='a', max_length=10),
            preserve_default=False,
        ),
    ]
