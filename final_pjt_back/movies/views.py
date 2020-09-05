from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Movie, Genre, Rate
from .serializers import MovieSerializer, GenreSerializer, RateSerializer
from accounts.serializers import UserSerializer

from django.contrib.auth import get_user_model
from django.db.models import Q

from django.core.paginator import Paginator

import random







User=get_user_model()





# 추천 알고리즘 넣을 자리
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_recommend(request,user_name):
    user = get_object_or_404(User, username=user_name)
    print(user)
    # rate = get_object_or_404(Rate, user=user)
    rate =Rate.objects.filter(user=user)
    rateserializer = RateSerializer(rate, many=True)
    # print(rateserializer.data)
    genreList=[]
    tmp_list=[]
    genre_idlist=[]

    for rate in rateserializer.data:
        tmp_list.append(rate['movie']['genres'])
        # print(rate['movie']['genres'])
    # print(tmp_list)

    if len(tmp_list)==0:
        return Response()

    for i in (tmp_list[0]):
        # print(i['name'])
        genreList.append(i['name'])
    # print(genreList)

    genres=Genre.objects.filter(name__in=genreList)
    genreserializer = GenreSerializer(genres,many=True)

    rec_movies = Movie.objects.filter(genres__name__in=genreList).order_by('-vote_average').distinct()[:10]

        

    serializer = MovieSerializer(rec_movies, many=True)
    return Response(serializer.data)



# 페이지
@api_view(['GET'])
def movie_split(request,sort_type,page_num):

    # d-기본
    # n-ewest
    # p-opul
    # r-ecommended
    # s-rating
    if sort_type=='d':
        FMovie = Movie.objects.all()
    if sort_type=='n':
        FMovie = Movie.objects.all().order_by('-release_date')
    if sort_type=='p':
        FMovie = Movie.objects.all().order_by('-popularity')
    if sort_type=='r':
        FMovie = Movie.objects.all().order_by('-id')
        # 다른 코드로 만들 것
        # 아직 완성하지 않았습니다.
    if sort_type=='s':
        FMovie = Movie.objects.all().order_by('-vote_average')

    movie_length = len(FMovie)


    num_per_page = 20

    if num_per_page*(page_num-1) <= movie_length <=num_per_page*(page_num)-1:
        movies = FMovie[num_per_page*(page_num-1):movie_length]
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)


    if num_per_page*(page_num)-1 >= movie_length:
        return Response()
    

    movies = FMovie[num_per_page*(page_num-1):num_per_page*(page_num)]



    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def movie_search(request,keyword):
    movies = Movie.objects.filter(title__icontains=keyword)
    if len(movies)==0:
        movies = Movie.objects.filter(original_title__icontains=keyword)


    serializer = MovieSerializer(movies, many=True)

    return Response(serializer.data)



@api_view(['GET'])
def movielist(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def modify(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_superuser==False:
        return Response()

    if request.method == 'GET':
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        temp = serializer.initial_data
        movie.title = temp['title']
        movie.content = temp['overview']
        movie.save()
    return Response()



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create(request):
    if request.user.is_superuser==False:
        return Response()
    print('check')
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        print('valid?')
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete(request, movie_pk):
    if request.user.is_superuser==False:
        return Response()

    movie = get_object_or_404(Movie, pk=movie_pk)
    movie.delete()

    return Response()






@api_view(['GET'])
def ratelist(request,movie_pk):
    target_movie = get_object_or_404(Movie, pk=movie_pk)
    rates = Rate.objects.filter(movie=target_movie)
    serializer = RateSerializer(rates, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_create(request,movie_pk):
    target_movie = get_object_or_404(Movie, pk=movie_pk)

    # if get_object_or_404(Rate, movie=target_movie ,user=request.user):
    #     print('이미 평가했음')
    #     return Response()
    if Rate.objects.filter(movie=target_movie ,user=request.user):
        print('이미 평가했음')
        return Response()
    
    serializer = RateSerializer(data=request.data)

    # temp = serializer.initial_data

    adding_score = serializer.initial_data['score']

    if serializer.is_valid(raise_exception=True):

        target_movie.vote_count +=1
        total_score = target_movie.vote_count * target_movie.vote_average
        total_score += int(adding_score)
        target_movie.vote_average = (total_score) / (target_movie.vote_count)

        target_movie.save()

        serializer.save(movie=target_movie,user=request.user)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_modify(request,movie_pk,rate_id):
    # print('수정')
    movie = get_object_or_404(Movie, pk=movie_pk)
    rate = get_object_or_404(Rate, id=rate_id)
    # print("수정2")
    serializer = RateSerializer(data=request.data)
    temp = serializer.initial_data
    # print(temp)

    pre_score = rate.score
    after_score = int(temp['score'])

    total_score = movie.vote_count * movie.vote_average

    total_score = total_score -pre_score + after_score

    movie.vote_average = (total_score) / (movie.vote_count)
    movie.save()

    rate.score = temp['score']
    rate.content = temp['content']
    rate.save()
    
    return Response()



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_delete(request,movie_pk,rate_id):
    movie = get_object_or_404(Movie, pk=movie_pk)
    rate = get_object_or_404(Rate, movie=movie, id=rate_id)
    
    tmp_score = int(rate.score)

    


    if rate.user == request.user:
        total_score = movie.vote_count * movie.vote_average
        total_score = total_score - tmp_score
    
        movie.vote_count -=1
        if movie.vote_count==0:
            movie.vote_average=0
        else:
            movie.vote_average = (total_score) / (movie.vote_count)

        rate.delete()
        movie.save()

    return Response()


    # pre_score = rate.score
    # after_score = int(temp['score'])

    # total_score = movie.vote_count * movie.vote_average

    # total_score = total_score -pre_score + after_score

    # movie.vote_average = (total_score) / (movie.vote_count)
    # movie.save()



@api_view(['GET'])
def rated_check(request,movie_pk,user_name):
    user = get_object_or_404(User, username=user_name)
    movie = get_object_or_404(Movie, pk=movie_pk)
    rate = get_object_or_404(Rate, movie=movie, user=user)
    # rate = Rate.objects.filter(movie=movie,user=user)
    if rate:
        serializer = RateSerializer(rate)

        return Response(serializer.data)
        
    else:
        return Response()
    


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_rates(request,user_name):
    user = get_object_or_404(User, username=user_name)
    rate = Rate.objects.filter(user=user)
    serializer = RateSerializer(rate,many=True)

    return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def comment_delete(request, article_id, comment_id):
#     article = get_object_or_404(Article, id=article_id)
#     comment = get_object_or_404(Comment, id=comment_id)
#     if comment.user == request.user and comment.article==article:
#         comment.delete()
#     return Response()