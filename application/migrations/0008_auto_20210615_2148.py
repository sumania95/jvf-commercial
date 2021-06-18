# Generated by Django 3.1.6 on 2021-06-15 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_auto_20210615_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiving',
            name='date_checked',
        ),
        migrations.RemoveField(
            model_name='releasing',
            name='status',
        ),
        migrations.AddField(
            model_name='receiving',
            name='control_no',
            field=models.CharField(default='0000', max_length=200),
        ),
        migrations.AddField(
            model_name='releasing',
            name='category',
            field=models.CharField(choices=[('1', 'Sales'), ('2', 'Warranty'), ('3', 'Transfer')], default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='releasing',
            name='control_no',
            field=models.CharField(default='0000', max_length=200),
        ),
        migrations.AddField(
            model_name='releasing',
            name='customer_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='releasing',
            name='others',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='releasing',
            name='purchase_order_number',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='receiving_detail',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]