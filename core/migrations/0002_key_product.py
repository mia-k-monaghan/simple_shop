# Generated by Django 3.1.3 on 2021-04-15 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('TS', 'Stripe Test Secret Key'), ('TP', 'Stripe Test Publishable Key'), ('LS', 'Stripe Live Secret Key'), ('LP', 'Stripe Live Publishable Key')], max_length=255)),
                ('key', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price_id', models.CharField(help_text='The Stripe Price ID for the product', max_length=255, unique=True)),
            ],
        ),
    ]
