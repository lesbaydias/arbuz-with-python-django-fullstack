# Generated by Django 4.1.7 on 2023-05-13 11:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('landing', '0005_basketitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_Card',
            fields=[
                ('cardholder_name', models.CharField(max_length=100)),
                ('card_number', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('expiration_year', models.IntegerField()),
                ('expiration_month', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('cvv', models.CharField(max_length=4)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment_cards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
