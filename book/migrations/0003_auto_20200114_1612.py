# Generated by Django 2.2.9 on 2020-01-14 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("book", "0002_auto_20200113_1958")]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="cover",
            field=models.URLField(blank=True, null=True),
        )
    ]