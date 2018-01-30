print "*"*25 + " URLS.PY " + "*"*25

from django.conf.urls import url
from . import views

urlpatterns = [
    url( r'^$', views.index ),
    url( r'^signup$', views.signup ),
    url( r'^login$', views.login ),
    url( r'^logout$', views.logout ),
    url( r'^books$', views.books ),
    url( r'^books_all$', views.books_all ),
    url( r'^books/(?P<id>\d+)/show$', views.book_show ),
    url( r'^books_and_reviews/new$', views.books_and_reviews_new ),
    url( r'^books_and_reviews/create$', views.books_and_reviews_create ),
    url( r'^reviews/(?P<id>\d+)/create$', views.review_create ),
    url( r'^reviews/(?P<id>\d+)/destroy$', views.review_destroy ),
    url( r'^users/(?P<id>\d+)/show$', views.user_show ),
]