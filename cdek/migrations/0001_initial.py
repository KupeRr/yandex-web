# Generated by Django 3.2.5 on 2022-11-15 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CdekPoint',
            fields=[
                ('point_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.point')),
                ('code', models.CharField(max_length=10)),
                ('active_status', models.BooleanField()),
                ('region_name', models.CharField(max_length=100)),
                ('city_code', models.CharField(max_length=20)),
                ('city_name', models.CharField(max_length=20)),
                ('work_time', models.CharField(max_length=300)),
                ('address', models.CharField(max_length=300)),
                ('full_address', models.CharField(max_length=1000)),
                ('phone_number', models.CharField(max_length=13)),
                ('note', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            bases=('core.point',),
        ),
    ]
