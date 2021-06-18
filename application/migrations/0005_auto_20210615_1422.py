# Generated by Django 3.1.6 on 2021-06-15 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20210614_2331'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receiving',
            old_name='date',
            new_name='date_checked',
        ),
        migrations.RemoveField(
            model_name='receiving',
            name='delivery_description',
        ),
        migrations.AddField(
            model_name='receiving',
            name='invoice_no',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='receiving',
            name='shipped_via',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='receiving',
            name='vendor',
            field=models.CharField(default='JVF', max_length=200),
        ),
    ]