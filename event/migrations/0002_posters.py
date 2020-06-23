# Generated by Django 3.0.5 on 2020-06-23 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster', models.ImageField(blank=True, upload_to='images')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_poster', to='event.Event')),
            ],
        ),
    ]
