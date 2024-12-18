# Generated by Django 5.1.2 on 2024-11-04 13:35

import auctions.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, validators=[auctions.models.validate_profanity])),
                ('description', models.CharField(max_length=1000, validators=[auctions.models.validate_profanity])),
                ('value', models.DecimalField(decimal_places=2, max_digits=12, validators=[auctions.models.validate_price])),
                ('image', models.URLField(blank=True, null=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
