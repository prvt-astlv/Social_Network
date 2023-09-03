from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from . import models
from accounts.models import Profile
from .forms import PostForm, CommentForm
from django.views import generic


def AllView(request):
    if request.user.is_authenticated:
        posts = []
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            profile = Profile.objects.create(user=request.user)
            profile.save()
        for user in profile.follows.all():
            posts.append(models.Post.objects.filter(user=user))
        if request.method == 'POST':
            description = request.POST.get('description')
            # image = request.POST.get('image')
            _, image = request.FILES.popitem()
            image = image[0]
            post = models.Post.objects.create(image=image, description=description, user=request.user.profile)
            post.save()
            return redirect('home')
        elif request.method == "POST" and request.action == 'post_comment':
            form = CommentForm(request.POST)
            if form.is_valid():
                form.save()
        comments = []
        for objects in posts:
            for post  in objects:
                comments.append(models.Comment.objects.filter(post=post))
        return render(request, 'home.html', context={"posts": posts, "comments": comments})
    else:
        return redirect('login')


def AboutView(request, pk):
    if request.user.is_authenticated is None:
        return redirect('login')
    else:
        post = models.Post.objects.get(pk=pk)
        comments = models.Comment.objects.filter()
        return render(request, 'about.html', context={'post': post, 'comments': comments})


def EditView(request):
    if request.user.is_authenticated is None:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = PostForm()
            if form.is_valid():
                form = PostForm(request.POST)
            return render(request, 'adbout.html', context={"form": form})


class DeleteView(generic.edit.DeleteView):
    model = models.Post
    success_url = reverse_lazy('home')
    template_name = 'delete.html'


def LikeView(request, pk):
    post = get_object_or_404(models.Post, id=request.POST.get('post_id'))

    liked = False
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('about', args=[str(pk)]))
