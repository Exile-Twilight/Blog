from django.conf.urls import url
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from app_blog.views import (
    IndexView, CategoryView, TagView,
    PostDetailView, SearchView, AuthorView
)
from app_blog.rss import LatestPostFeed
from app_blog.sitemap import PostSitemap
from app_blog.apis import PostViewSet,CategoryViewSet
# from app_blog.apis import post_list, PostList
from app_comment.views import CommentView
from app_config.views import LinkListView
from .custom_site import custom_site

"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
router = DefaultRouter()
router.register(r'post', PostViewSet, basename='api-post')
router.register(r'category', CategoryViewSet, basename='api-category')

urlpatterns = [
    url(r'^super_admin/', admin.site.urls, name='super-admin'),
    url(r'^api/', include(router.urls)),
    url(r'^api/docs/', include_docs_urls(title='Blog apis')),
    # url(r'^api/post/', post_list, name='post-list'),
    # url(r'^api/post/', PostList.as_view(), name='post-list'),
    url(r'^admin/', custom_site.urls, name='admin'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name="tag-list"),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(), name='post-detail'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemap': {'posts': PostSitemap}}),

]
