# Generated by Django 5.0.2 on 2024-02-15 07:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Phonebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('surname', models.CharField(db_index=True, max_length=100)),
                ('middle_name', models.CharField(max_length=100)),
                ('employee_phone_number', models.CharField(max_length=20, unique=True)),
                ('mobile_phone_number', models.CharField(max_length=20, unique=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phonebook.organization')),
            ],
        ),
    ]
