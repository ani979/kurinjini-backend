# Generated by Django 2.2.2 on 2019-07-12 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbe', '0002_auto_20190712_0238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(editable=False, max_length=9, primary_key=True, serialize=False),
        ),
    ]
