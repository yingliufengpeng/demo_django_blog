"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views import static
from demo import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r"^uploads/(?P<path>.*)$", static.serve, {"document_root": settings.MEDIA_ROOT}),
    url(r"^login/", views.login, name='login'),
    url(r"^logout/", views.logout, name='logout'),
    url(r"^register/", views.register, name='register'),
    url(r"^index/", views.index, name='index'),
    url(r"^home/", views.home, name='home'),
    url(r"^article/", views.article, name='article'),
    url(r"^add_article/", views.add_article, name='add_article'),
    url(r"^upload_img/", views.upload_img, name='upload_img'),
    url(r"^article_ajax_add/", views.article_ajax_add, name='article_ajax_add'),
    url(r"^modify_article/", views.modify_article, name='modify_article'),
    url(r"^article_ajax_modify/", views.article_ajax_modify, name='article_ajax_modify'),
    url(r"^article_ajax_delete/", views.article_ajax_delete, name='article_ajax_delete'),
]
