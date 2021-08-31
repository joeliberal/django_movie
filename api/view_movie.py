from rest_framework.response import Response
from movie.models import Movie
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.urls import reverse
from .serializer_movie import (
                MovieChoiceListSerializer, MovieAllListSerializer,
                MovieDetailDataSerializer, MovieSerializer
)


@api_view(['GET'])
def movie_list(request, choice):
    paginator = PageNumberPagination()
    paginator.page_size = 12
    
    video = Movie.objects.filter(choice = choice)

    result_page = paginator.paginate_queryset(video ,request)

    srz = MovieChoiceListSerializer(result_page, many=True).data

    return paginator.get_paginated_response(srz)


@api_view(['GET'],)
def movie_detail(request, slug):
    video = Movie.objects.get(slug=slug)

    srz_detail = MovieSerializer(video).data

    if not request.user.is_authenticated:
        srz_data = {'please login to account'}
    elif request.user.is_paid == True or request.user.is_admin:
        srz_data = MovieDetailDataSerializer(video).data
        if request.user.is_admin:
            link = {
                'edit_movie': reverse('api:movie_edit', args=[video.slug]),
                'create_review':reverse('api:create_review_movie', args =[video.pk])
            }
        else:
            link = None
    else:
        srz_data = {'Please proceed to purchase a subscription'}
     
    srz = (srz_data,srz_detail,link )

    return Response(srz, status=status.HTTP_200_OK)


@api_view(['GET'])
def movie_all_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 12

    video = Movie.objects.all()

    result_page = paginator.paginate_queryset(video, request)

    srz = MovieAllListSerializer(result_page, many=True).data

    return paginator.get_paginated_response(srz)


@api_view(['GET','POST'])
def movie_create(request):
    if request.method == 'POST':
        form = MovieSerializer(data = request.data)
        if form.is_valid():
            form.save()
            return Response(form.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.data, status=status.HTTP_400_BAD_REQUEST)

    else:
        form = MovieSerializer()
        return Response(form.data)



@api_view(["GET",'PUT'])
def movie_edit(request, slug):
    try:
        video = Movie.objects.get(slug=slug)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        form = MovieSerializer(video, data=request.data)
        if form.is_valid():
            form.save()
            return Response(video.data, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        form = MovieSerializer(video)
        return Response(form.data)

