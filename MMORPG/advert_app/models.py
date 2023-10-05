from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect


class Post(models.Model):
    """
    Модель для создания объявлений
    """
    tank = 'TN'  # танк
    heal = 'HL'  # хил
    damage_dealer = 'DD'  # дамагер
    trader = 'TR'  # торговец
    guild_master = 'GM'  # гилдмастер
    questgiver = 'QG'  # квестгивер
    blacksmith = 'BS'  # кузнец
    tanner = 'TN'  # кожевник
    poison_master = 'PM'  # зельевар
    spell_master = 'SM'  # мастер заклинаний

    SELECT = [
        (tank, 'Tанк'),
        (heal, 'Хил'),
        (damage_dealer, 'Дамагер'),
        (trader, 'Торговец'),
        (guild_master, 'Гилдмастер'),
        (questgiver, 'Квестгивер'),
        (blacksmith, 'Кузнец'),
        (tanner, 'Кожевник'),
        (poison_master, 'Зельевар'),
        (spell_master, 'Мастер заклинаний')
    ]

    post_title = models.CharField(max_length=250, default='Заголовок объявления', unique=True)
    post_text = models.TextField(default='Введите текст объявления')
    post_author = models.ForeignKey('Author', on_delete=models.CASCADE)
    post_category = models.CharField(max_length=2, choices=SELECT)
    post_image = models.ImageField(upload_to='images/', blank=True, null=True)
    post_time_in = models.DateTimeField(auto_now_add=True,)
    post_rating = models.IntegerField(default=0,)

    def __str__(self):
        return f'{self.post_title} {self.post_author}'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    """    Модель для создания откликов к объявлениям
    """
    comment_text = models.TextField(blank=True)
    comment_time_in = models.DateTimeField(auto_now_add=True)
    comment_to_post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_status = models.IntegerField(blank=True, null=True)  # для статуса отклика - для принятия или удаления


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        sum_author_rating = Post.objects.filter(post_author=self.id).values('post_rating')
        self.author_rating = sum([i['post_rating'] for i in sum_author_rating])

    def __str__(self):
        return f'{self.author}'
