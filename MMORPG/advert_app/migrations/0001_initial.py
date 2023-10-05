# Generated by Django 4.2.4 on 2023-09-01 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_rating', models.IntegerField(default=0)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_title', models.CharField(default='Заголовок объявления', max_length=250, unique=True)),
                ('post_text', models.TextField(default='Введите текст объявления')),
                ('post_category', models.CharField(choices=[('TN', 'танк'), ('HL', 'хил'), ('DD', 'дамагер'), ('TR', 'торговец'), ('GM', 'гилдмастер'), ('QG', 'квестгивер'), ('BS', 'кузнец'), ('TN', 'кожевник'), ('PM', 'зельевар'), ('SM', 'мастер заклинаний')], max_length=2)),
                ('post_time_in', models.DateTimeField(auto_now=True)),
                ('post_rating', models.IntegerField(default=0)),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advert_app.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(blank=True)),
                ('comment_time_in', models.DateTimeField(auto_now_add=True)),
                ('comment_status', models.IntegerField(blank=True)),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment_to_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advert_app.post')),
            ],
        ),
    ]
