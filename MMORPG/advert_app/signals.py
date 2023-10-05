import os

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Comment, Author, Post, User

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@receiver(post_save, sender=Comment)
def write_comment(sender, instance, created, update_fields, **kwargs):
    if created:
        post_id_comment = instance.comment_to_post_id
        post_author_id = Post.objects.get(id=post_id_comment)
        # получаем queryset из модели Author по комментарию к id посту для получения данных об авторе
        post_author_email_qs = Author.objects.filter(id=post_author_id.post_author_id)
        post_author_email = list(post_author_email_qs.values_list('author__email', flat=True))

        send_mail(
            subject=f'Новый комментарий к посту {post_author_id.post_title}',
            message=f'Пользователь {instance.comment_author} написал новый комментарий к вашему посту '
                    f'{post_author_id.post_title}\n'
                    f'Краткое содержание комментария: {instance.comment_text[:20]}',
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),
            recipient_list=post_author_email
        )
    else:
        comment_author_id = User.objects.filter(id=instance.comment_author_id)
        post_id = Post.objects.get(id=instance.comment_to_post_id)

        send_mail(
            subject=f'Ваш комментарий к посту {post_id.post_title} принят!',
            message=f'Здравствуйте {instance.comment_author}!\n'
                    f'Ваш комментарий {instance.comment_text[:30]} принят автором поста {post_id.post_author}',
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),
            recipient_list=list(comment_author_id.values_list('email', flat=True))
        )
