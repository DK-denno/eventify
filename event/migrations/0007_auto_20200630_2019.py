# Generated by Django 3.0.5 on 2020-06-30 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_tickets_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tickets',
            old_name='tickentNumber',
            new_name='ticketNumber',
        ),
    ]
