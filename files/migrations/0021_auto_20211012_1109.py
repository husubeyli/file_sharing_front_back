# Generated by Django 3.2.8 on 2021-10-12 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0020_auto_20211012_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='file',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]