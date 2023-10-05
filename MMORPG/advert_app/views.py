from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import Post, Author, Comment
from .forms import PostCreateForm, CommentCreateForm
from django.contrib.auth.models import User


class PostList(ListView):
    model = Post
    ordering = 'post_time_in'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = [i['comment_to_post_id'] for i in Comment.objects.all().values('comment_to_post_id')]
        if self.request.user.username in [i['author__username'] for i in Author.objects.all().values('author__username')]:
            context['author'] = Author.objects.get(author__username=self.request.user.username)
        context['is_author'] = self.request.user.username in [i['author__username'] for i in Author.objects.all().values('author__username')]
        return context


class PostCreateView(CreateView):  # модель для создания новостей
    form_class = PostCreateForm
    model = Post
    template_name = 'post_create.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(comment_to_post_id=self.kwargs['pk'])
        # создаем список существующих авторов и проверяем есть пользователь среди них
        list_authors = [i['author__username'] for i in Author.objects.all().values('author__username')]
        if self.request.user.username in list_authors:
            context['author'] = Author.objects.get(author__username=self.request.user.username)
        context['is_author'] = self.request.user.username in [i['author__username'] for i in
                                                              Author.objects.all().values('author__username')]
        return context


class CommentToPost(CreateView):
    form_class = CommentCreateForm
    model = Comment
    template_name = 'comment.html'
    success_url = '/posts/'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.comment_to_post = Post.objects.get(id=self.kwargs['pk'])
        comment.comment_author = User.objects.get(id=self.request.user.id)
        comment.comment_status = 0
        return super().form_valid(form)


def accept_comment(request, id_comment):  # принятие комментариев присваивая им статус = 1
    comment = Comment.objects.get(id=id_comment)
    comment.comment_status = 1
    comment.save()
    comment_id = Comment.objects.get(id=id_comment)
    return redirect(f'/posts/{comment_id.comment_to_post_id}')


def delete_comment(request, id_comment):  # удаление комментариев к посту
    comment = Comment.objects.get(id=id_comment)
    Comment.objects.get(id=id_comment).delete()
    return redirect(f'/posts/{comment.comment_to_post_id}')
