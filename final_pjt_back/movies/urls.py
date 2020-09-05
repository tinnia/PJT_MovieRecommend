from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movielist, name='movielist'),
    path('<str:user_name>/rates/', views.get_rates, name='get_rates'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/modify/', views.modify, name='modify'),
    path('create/', views.create, name='create'),
    path('<int:movie_pk>/delete/', views.delete, name='delete'), 
    path('<int:movie_pk>/rate/', views.ratelist, name='ratelist'),
    path('<int:movie_pk>/rate/create/', views.rate_create, name='rate_create'),
    path('<int:movie_pk>/rate/<int:rate_id>/modify/', views.rate_modify, name='rate_modify'),
    path('<int:movie_pk>/rate/<int:rate_id>/delete/', views.rate_delete, name='rate_delete'),
    path('<int:movie_pk>/ratedcheck/<str:user_name>/', views.rated_check, name='rated_check'),

    path('split/<str:sort_type>/<int:page_num>/',views.movie_split,  name='movie_split'),
    path('search/<str:keyword>/',views.movie_search,  name='movie_search'),
    path('<str:user_name>/recommends/',views.movie_recommend, name='movie_recommend'),
]


#  axios.get(`${BACK_URL}/movies/${this.movie_pk}/ratedcheck/${this.$cookies.get('username')}/`)