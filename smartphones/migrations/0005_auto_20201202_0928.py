# Generated by Django 3.1.4 on 2020-12-02 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartphones', '0004_smartphone_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartphone',
            name='img',
            field=models.ImageField(null=True, upload_to='uploads/%Y/%m/%d'),
        ),
    ]
