from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from accounts.serializers import UserSerializer

from articles.models import Article,Comment
from movies.models import Rate

import random

# Create your tests here.
User = get_user_model()

@api_view(['GET'])
def users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def disableuser(request, user_id):
    selected_user = get_object_or_404(User,id=user_id)
    if selected_user.is_active == True:
         selected_user.is_active = False
    else:
        selected_user.is_active = True
    selected_user.save()
    serializer = UserSerializer(selected_user)
    return Response(serializer.data)


@api_view(['GET'])
def getuserdetail(request, user_name):
    selected_user = get_object_or_404(User,username=user_name)
    serializer = UserSerializer(selected_user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def karma(request,user_name):
    user = get_object_or_404(User,username=user_name)
    karmalist=[]
    rate_tot=0

    if request.user != user:
        return Response()

    articles = Article.objects.filter(user=request.user)
    comments = Comment.objects.filter(user=request.user)
    rates = Rate.objects.filter(user=request.user)

    print(articles)
    print(comments)
    print(rates)





    if len(articles): 
        if len(articles)>=5:
            karmalist.append(('리뷰를 많이 쓴',len(articles)))
        else:
            karmalist.append(('리뷰를 쓴',len(articles)))


        for article in articles:

            if len(article.content)>=300:
                karmalist.append(('장문의 글을 써본',len(article.content)))

            if len(article.content)<=6:
                karmalist.append(('짧은 글을 써본',len(article.content)*50))






    if len(comments):
        if len(comments)>=5:
            karmalist.append(('댓글을 많이 쓴',len(comments)))

        else:
            karmalist.append(('댓글을 쓴',len(comments)))    







    if len(rates):
        if len(rates)>=5:
            karmalist.append(('평점을 많이 적은',len(rates)))

        else:
            karmalist.append(('평점을 쓴',len(rates)))

        
        for rate in rates:

            rate_tot +=rate.score
 

        if rate_tot/len(rates) >=8:
            karmalist.append(('평점이 후한',rate_tot*10/len(rates)))

        if rate_tot/len(rates) <=4:
            karmalist.append(('평점이 박한',rate_tot*20/len(rates)))



    if len(karmalist)==0:
        return Response()


    
    karma = sorted(karmalist, key=lambda x:x[1], reverse=True)
    print(karma)
    
    if karma[0][1] > karma[1][1] + 120:

        user.karma = karma[0][0]
        

    else:

        tmp=random.sample(karma,1)

        user.karma=tmp[0][0]

    user.save()




    return Response()