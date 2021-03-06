# Generated by Django 3.1.3 on 2021-04-15 20:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('fulfilled', models.BooleanField(default=False)),
                ('address1', models.CharField(max_length=100, null=True)),
                ('address2', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('state', localflavor.us.models.USStateField(max_length=2, null=True)),
                ('zip', localflavor.us.models.USZipCodeField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=250, null=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('active', models.BooleanField(default=False)),
                ('fulfilled', models.BooleanField(default=False)),
                ('address1', models.CharField(max_length=100, null=True)),
                ('address2', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('state', localflavor.us.models.USStateField(max_length=2, null=True)),
                ('zip', localflavor.us.models.USZipCodeField(max_length=10, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
