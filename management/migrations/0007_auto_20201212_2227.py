# Generated by Django 3.1.3 on 2020-12-13 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_auto_20201212_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerhistory',
            name='group',
        ),
        migrations.AlterField(
            model_name='customer',
            name='group',
            field=models.CharField(choices=[('WHOLESALER', 'WHOLESALER'), ('SPECIALIZED CUSTOMER', 'SPECIALIZED CUSTOMER'), ('RETAIL', 'RETAIL'), ('BOOKSHOP', 'BOOKSHOP'), ('SCHOOL', 'SCHOOL'), ('OTHERS', 'OTHERS'), ('AGENT', 'AGENT')], max_length=100),
        ),
    ]
