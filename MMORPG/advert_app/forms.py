from django import forms
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['post_title'].label = 'Заголовок'
    #     self.fields['post_category'].label = 'Категория'

    class Meta:
        model = Post
        fields = ['post_title', 'post_text', 'post_author', 'post_category', 'post_image']


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
