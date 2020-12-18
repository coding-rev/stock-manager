# Generated by Django 3.1.3 on 2020-12-13 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='group',
            field=models.CharField(choices=[('BOOKSHOP', 'BOOKSHOP'), ('WHOLESALER', 'WHOLESALER'), ('SCHOOL', 'SCHOOL'), ('SPECIALIZED CUSTOMER', 'SPECIALIZED CUSTOMER'), ('AGENT', 'AGENT'), ('RETAIL', 'RETAIL'), ('OTHERS', 'OTHERS')], max_length=100),
        ),
        migrations.AlterField(
            model_name='customerhistory',
            name='group',
            field=models.CharField(choices=[('BOOKSHOP', 'BOOKSHOP'), ('WHOLESALER', 'WHOLESALER'), ('SCHOOL', 'SCHOOL'), ('SPECIALIZED CUSTOMER', 'SPECIALIZED CUSTOMER'), ('AGENT', 'AGENT'), ('RETAIL', 'RETAIL'), ('OTHERS', 'OTHERS')], max_length=100),
        ),
    ]
