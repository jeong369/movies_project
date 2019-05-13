# Generated by Django 2.1.8 on 2019-05-13 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_remove_genre_like_people'),
        ('accounts', '0004_user_like_movies'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='like_genres',
            field=models.ManyToManyField(blank=True, related_name='like_users', to='movies.Genre'),
        ),
    ]
