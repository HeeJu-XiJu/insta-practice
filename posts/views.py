from django.shortcuts import render, redirect
from .models import Post
from .form import PostForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-id')

    context = {
        'posts': posts,
    }
    return render(request, 'index.html', context)


def create(request):
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'form.html', context)

@login_required
def likes(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    # 이미 좋아요 버튼을 누른 경우
    if post in user.like_posts.all():
        post.like_users.remove(user)
    # 좋아요 버튼을 아직 안 누른 경우
    else:
        post.like_users.add(user)
        # user.like_posts.add(post)
    return redirect('posts:index')


def likes_async(request, id):
    user = request.user
    post = Post.objects.get(id=id)
    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False
    else:
        post.like_users.add(user)
        status = True
    context = {
        'status': status,
        'count': len(post.like_users.all()),
    }
    return JsonResponse(context)