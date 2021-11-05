from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from core.time_func import timeit

from yatube.settings import YATUBE_CONST

from .forms import PostForm
from .models import Group, Post, User


@timeit
def index(request):
    template = 'posts/index.html'
    text = 'Это главная страница проекта Yatube'
    posts = Post.objects.select_related('group', 'author').all()
    paginator = Paginator(posts, YATUBE_CONST['count_pag'])
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'text': text,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@timeit
def group_posts(request, slug):
    template = 'posts/group_list.html'
    text = 'Здесь будет информация о группах проекта Yatube'
    group = Group.objects.get(slug=slug)
    posts = group.group_posts.all().select_related('author')
    paginator = Paginator(posts, YATUBE_CONST['count_pag'])
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'text': text,
        # 'group': group,
        # 'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@timeit
def profile(request, username):
    template = 'posts/profile.html'
    author = User.objects.get(username=username)
    posts = author.posts.all().select_related('group', 'author')
    paginator = Paginator(posts, YATUBE_CONST['count_pag'])
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'author': author,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, template, context)


@timeit
def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = Post.objects.select_related('group', 'author').get(id=post_id)
    username = post.author.username
    author = get_object_or_404(User, username=username)
    count = author.posts.all().count()
    context = {
        'post': post,
        'count': count,
    }
    return render(request, template, context)


@timeit
@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user.username)
    return render(request, template, {'form': form})


@timeit
@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    is_edit = True
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id)
    if form.is_valid():
        post.save(force_update=True)
        return redirect('posts:post_detail', post_id=post.id)
    return render(
        request, template, {'form': form, 'is_edit': is_edit, 'post': post})
