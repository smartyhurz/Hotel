# Generated by Django 5.0.7 on 2024-08-18 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visom6', '0008_hall'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='hall',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='visom6.hall'),
        ),
    ]
