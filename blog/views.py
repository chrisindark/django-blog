from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from accounts.models import User
from accounts.forms import FileForm
from blog.decorators import user_is_post_owner

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


# Create your views here.
class PostListView(ListView):
    # queryset = Post.objects.all()
    model = Post
    template_name = 'blog/post_list.html'
    ordering = '-created_date'
    # paginate_by = 5
    # context_object_name = 'posts'

    def get_queryset(self):
        return super(PostListView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        # context['posts'] = context['post_list']
        return context


# def post_list(request):
#     queryset = Post.objects.all()
#     page = request.GET.get('page', 1)
#     paginator = Paginator(queryset, 1)
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, 'blog/post_list.html', {'posts': posts})


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


# @login_required
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#
#     return render(request, 'blog/post_edit.html', {'form': form})


class PostDetailView(DetailView):
    # queryset = Post.objects.all()
    model = Post
    template_name = 'blog/post_detail.html'
    # context_object_name = 'post'

    def get_queryset(self):
        return self.model.objects.all().select_related('author')

    def get(self, request, *args, **kwargs):
        return super(PostDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        return context


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     return render(request, 'blog/post_detail.html', {'post': post})


@method_decorator(user_is_post_owner, name='dispatch')
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm

    # def form_valid(self, form):
    #     """
    #     If the form is valid, save the associated model.
    #     """
    #     form.instance.author = self.request.user
    #     return super(PostUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#
#     return render(request, 'blog/post_edit.html', {'form': form})


@method_decorator(user_is_post_owner, name='dispatch')
@method_decorator(login_required, name='dispatch')
class PostPublishView(UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.published_date = timezone.now()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


# @login_required
# def post_publish(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     return redirect('post_detail', pk=pk)


@method_decorator(login_required, name='dispatch')
class PostDraftListView(ListView):
    model = Post
    template_name = 'blog/post_draft_list.html'
    ordering = '-created_date'

    def get_queryset(self):
        return self.model.objects.filter(
            published_date__isnull=True,
            author=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super(PostDraftListView, self).get_context_data(**kwargs)
        return context


# @login_required
# def post_draft_list(request):
#     posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
#
#     return render(request, 'blog/post_draft_list.html', {'posts': posts})


@method_decorator(user_is_post_owner, name='dispatch')
@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_detail.html'

    def delete(self, request, *args, **kwargs):
        # self.get_object().delete()
        return HttpResponseRedirect(self.get_success_url())
        # super(PostDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.delete()
#
#     return redirect('post_list')


class PostCommentCreateView(CreateView):
    model = Comment
    template_name = 'blog/comment_create.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = None
        self.post = get_object_or_404(Post, pk=kwargs.get('post_id'))
        return super(PostCommentCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        form.instance.author = self.request.user
        form.instance.post = self.post
        print('here')
        return super(PostCommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})


# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#
#     return render(request, 'blog/comment_create.html', {'form': form})
#
#
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
