from django.shortcuts import render
from .models import Movie, Rating, User
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user

            try:
                rating = Rating.objects.get(movie=movie, user=user)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': "Rating updated", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating(stars=stars, movie=movie, user=user)
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': "Rating created", 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)


        else:
            response = {'message': "You need to provide stars"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response = {'message': "You can't update rating this way"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': "You can't create rating this way"}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
