# Generated by Django 2.1.8 on 2019-05-13 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_genre_like_people'),
        ('accounts', '0003_remove_user_like_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='like_movies',
            field=models.ManyToManyField(related_name='like_users', to='movies.Movie'),
        ),
    ]