# Generated by Django 2.2.9 on 2020-02-29 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("book", "0003_auto_20200114_1612")]

    operations = [
        migrations.AlterModelOptions(
            name="book", options={"permissions": (("manage_books", "Manage books."),)}
        )
    ]