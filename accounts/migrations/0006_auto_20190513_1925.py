# Generated by Django 2.1.8 on 2019-05-13 10:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_user_like_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='like_movies',
            field=models.ManyToManyField(blank=True, related_name='like_users', to='movies.Movie'),
        ),
    ]
