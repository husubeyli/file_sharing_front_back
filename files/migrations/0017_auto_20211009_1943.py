# Generated by Django 3.2.8 on 2021-10-09 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0016_rename_user_comment_users'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accessuser',
            options={'verbose_name': 'Access user', 'verbose_name_plural': 'Access users'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ManyToManyField(blank=True, null=True, related_name='_files_comment_parent_+', to='files.Comment'),
        ),
    ]
