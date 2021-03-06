# Generated by Django 2.2.9 on 2020-01-13 19:58

import book.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("book", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="book",
            name="cover",
            field=models.ImageField(blank=True, null=True, upload_to="book_covers/"),
        ),
        migrations.AddField(
            model_name="book",
            name="number_of_pages",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="books",
                to="book.Author",
            ),
        ),
        migrations.AlterField(
            model_name="usertobook",
            name="rate",
            field=models.PositiveIntegerField(
                blank=True,
                choices=[
                    (1, 1),
                    (2, 2),
                    (3, 3),
                    (4, 4),
                    (5, 5),
                    (6, 6),
                    (7, 7),
                    (8, 8),
                    (9, 9),
                ],
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="usertobook",
            name="status",
            field=models.CharField(
                choices=[
                    (book.models.BookStatuses("read"), "Read"),
                    (book.models.BookStatuses("to_read"), "To read"),
                ],
                default=book.models.BookStatuses("to_read"),
                max_length=20,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="book", unique_together={("title", "author")}
        ),
    ]
