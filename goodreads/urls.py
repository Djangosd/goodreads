import patterns as patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.template.defaulttags import url
from django.urls import path, include, re_path

import os

from books.views import BooksView
from .views import landing_page, home_page, shopping_page, community_page, notice_page, telephone_page

from django.views.static import serve

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("home/", home_page, name="home_page"),
    path("users/", include("users.urls")),
    path("books/", include("books.urls")),
    path("api/", include("api.urls")),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path("shopping/", shopping_page, name="shopping_page"),
    path("community/", community_page, name="community_page"),
    path("notice/", notice_page, name="notice_page"),
    path("telephone/", telephone_page, name="telephone_page"),

    path("", BooksView.as_view(), name="list"),


    # url(r'^media/(?P<path>.*)$', serve,{'document_root':  settings.MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

