from django.conf.urls import url
from blog import views

urlpatterns = [
    # url(r'^$', views.post_list, name='post_list'),
    url(r'^$', views.PostListView.as_view(), name='post_list'),

    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),

    # url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^post/(?P<pk>\d+)/delete', views.PostDeleteView.as_view(), name='post_delete'),

    # url(r'^post/new/$', views.post_new, name='post_create'),
    url(r'^post/create', views.PostCreateView.as_view(), name='post_create'),

    # url(r'^post/(?P<pk>\d+)/update/$', views.post_edit, name='post_update'),
    url(r'^post/(?P<pk>\d+)/update/$', views.PostUpdateView.as_view(), name='post_update'),

    # url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.PostPublishView.as_view(), name='post_publish'),

    # url(r'^post/drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/drafts/$', views.PostDraftListView.as_view(), name='post_draft_list'),

    # url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='post_comment_create'),
    url(r'^post/(?P<post_id>\d+)/comment/$', views.PostCommentCreateView.as_view(), name='post_comment_create'),

    # url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    # url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
]
