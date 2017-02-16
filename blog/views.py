# from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.

def post_list(request):
    # post_list = Post.objects.filter(created_date__isnull=False).order_by('-updated_date')
    queryset = Post.objects.select_related('author').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 1)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # print(form)
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')

    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return redirect('post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()

    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/add_comment_to_post.html', {'form': form})


# @login_required
# def comment_approve(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#
#     return redirect('blog.views.post_detail', pk=comment.post.pk)
#
#
# @login_required
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     post_pk = comment.post.pk
#     comment.delete()
#
#     return redirect('blog.views.post_detail', pk=post_pk)


@csrf_exempt
def user_upload(request):
    # Handle file upload
    if request.method == 'POST':
        print('\n\n')
        print(request.POST)
        print('\n\n')
        print(request.FILES)
        print('\n\n')
        print(request.user)
        form = FileForm(request.POST, request.FILES)
        print('\n\n')
        print(form)
        user = User.objects.get(email__iexact='christopherp@mindfiresolutions.com')
        print(user)
        if form.is_valid():
            userfile = form.save(commit=False)
            userfile.user = user
            userfile.save()
            print('\n\n')
            print(userfile)

            file = File(content_object=userfile, file=request.FILES['file'])
            file.save()

            return JsonResponse({
                'success': 'Success!',
                # 'file': newfile
            })
        else:
            print(form)
    # else:
    #     form = DocumentForm() # A empty, unbound form
    #     