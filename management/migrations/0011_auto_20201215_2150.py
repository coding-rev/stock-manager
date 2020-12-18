# Generated by Django 3.1.3 on 2020-12-16 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0010_auto_20201212_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerhistory',
            name='debt',
        ),
        migrations.AddField(
            model_name='customerhistory',
            name='paying',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='group',
            field=models.CharField(choices=[('OTHERS', 'OTHERS'), ('SPECIALIZED CUSTOMER', 'SPECIALIZED CUSTOMER'), ('SCHOOL', 'SCHOOL'), ('RETAIL', 'RETAIL'), ('WHOLESALER', 'WHOLESALER'), ('BOOKSHOP', 'BOOKSHOP'), ('AGENT', 'AGENT')], max_length=100),
        ),
    ]
