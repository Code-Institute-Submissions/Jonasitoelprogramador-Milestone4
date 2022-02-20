# Generated by Django 3.2 on 2022-02-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220123_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='payment_status',
            field=models.CharField(choices=[('paid', 'paid'), ('nonpaid', 'nonpaid')], default='nonpaid', max_length=10),
        ),
        migrations.AddField(
            model_name='worker',
            name='payment_status',
            field=models.CharField(choices=[('paid', 'paid'), ('nonpaid', 'nonpaid')], default='nonpaid', max_length=10),
        ),
    ]
