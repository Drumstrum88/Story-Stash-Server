"""
URL configuration for storystash project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from storystashapi.views.auth import check_user, register_user
from storystashapi.views.book_views import BookView, search_books
from storystashapi.views.genre_views import GenreView
from storystashapi.views.review_views import ReviewView
from storystashapi.views.stash_book_views import StashBookView
from storystashapi.views.stash_views import StashView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'books', BookView, 'book' )
router.register(r'genres', GenreView, 'genre')
router.register(r'stashes', StashView, 'stash')
router.register(r'stashbooks', StashBookView, 'stashbook')
router.register(r'reviews', ReviewView, 'Review')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('checkuser', check_user),
    path('registeruser', register_user),
    path('', include(router.urls)),
    path('books/list_filtered_by_genre/', BookView.as_view({'get': 'list_filtered_by_genre'}), name='list_filtered_by_genre'),
    path('books/search/', search_books, name='search_books'),
    path('stashbooks/read/', StashBookView.as_view({'get': 'get_read_books_for_user'}), name='read_stashbooks'),
    path('stashbooks/get_read_books_for_user/', StashBookView.as_view({'get': 'get_read_books_for_user'}), name='get_read_books_for_user'),
]


