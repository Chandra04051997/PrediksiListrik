# Generated by Django 3.1 on 2020-08-15 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_auto_20200812_0455'),
    ]

    operations = [
        migrations.CreateModel(
            name='dataCSV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_tahun', models.IntegerField()),
                ('nama_bulan', models.CharField(max_length=255)),
                ('data_content', models.FloatField()),
                ('nama_item', models.CharField(max_length=255)),
            ],
        ),
    ]
