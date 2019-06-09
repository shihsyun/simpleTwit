from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from django.http import JsonResponse
from django.db import IntegrityError
from django.utils import timezone
from .serializers import AuthUserSerializer, TwitSerializer
from .models import AuthUser, AuthToken, Twit, Comment
from .decorators import login_required
import json
from django.core import serializers


@api_view(['POST'])
def Register(request):

    data = JSONParser().parse(request)
    serializer = AuthUserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'User email: {}'.format(serializer.data['email'])}, status=HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Login(request):

    data = JSONParser().parse(request)

    if AuthUser.objects.verify_password(data['email'], data['password']):
        user = AuthUser.objects.get(email=data['email'])
        if user is None:
            return JsonResponse(data, status=HTTP_400_BAD_REQUEST)

        token = AuthToken.objects.create(user)
        token.save()
        user.last_login = timezone.now()
        user.save()
        return Response(token.code, status=HTTP_200_OK)

    return JsonResponse(data, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required()
def Logout(request):
    if AuthToken.objects.remove(request.session['user_token']):
        del request.session['user_id']
        return Response(status=HTTP_204_NO_CONTENT)

    return Response(status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required()
def CreateTwit(request):

    user = AuthUser.objects.get(
        id=request.session['user_id'])
    data = JSONParser().parse(request)

    twit = Twit.objects.create(user=user, text=data['content'])
    twit.save()
    return Response({'New twit {} is created at {}'.format(twit.content, twit.created_at)}, status=HTTP_201_CREATED)


@api_view(['POST'])
@login_required()
def CreateComment(request):

    user = AuthUser.objects.get(
        id=request.session['user_id'])
    data = JSONParser().parse(request)

    twit = Twit.objects.get(id=data['twit_id'])

    comment = Comment.objects.create(
        user=user, twit=twit, text=data['content'])
    comment.save()
    return Response({'New Comment {} is created at {}'.format(comment.content, comment.created_at)}, status=HTTP_201_CREATED)


@api_view(['POST'])
@login_required()
def CreateLikeit(request):

    user = AuthUser.objects.get(
        id=request.session['user_id'])
    data = JSONParser().parse(request)

    twit = Twit.objects.get(id=data['twit_id'])

    twit.likeit.add(user)

    return Response({}, status=HTTP_201_CREATED)


@api_view(['DELETE'])
@login_required()
def DestoryLikeit(request):

    user = AuthUser.objects.get(
        id=request.session['user_id'])
    data = JSONParser().parse(request)

    twit = Twit.objects.get(id=data['twit_id'])

    twit.likeit.remove(user)

    return Response({}, status=HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@login_required()
def TwitDetail(request, pk):

    try:
        twit = Twit.objects.get(id=pk)
    except Twit.DoesNotExist:
        return Response({}, status=HTTP_400_BAD_REQUEST)

    if request.method == 'GET':

        try:
            comment = Comment.objects.get(twit=twit)
        except Comment.DoesNotExist:
            return JsonResponse({'Twit': twit.content}, status=HTTP_200_OK)

        try:
            twits = Twit.objects.filter(id=pk)
        except Twit.DoesNotExist:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        data = serializers.serialize('json', twits)
        print(data)

        return JsonResponse({'Twit': twit.content}, status=HTTP_200_OK)

    if request.method == 'DELETE':
        if twit.user_id == request.session['user_id']:
            twit.delete()
            return Response({}, status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        if twit.user_id == request.session['user_id']:
            data = JSONParser().parse(request)
            twit = Twit.objects.update(twit=twit, text=data['content'])
            twit.save()
            return Response({}, status=HTTP_204_NO_CONTENT)

    return Response({}, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@login_required()
def CommentDetail(request, pk):

    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response({}, status=HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        return JsonResponse({'Comment': comment.content}, status=HTTP_200_OK)

    if request.method == 'DELETE':
        if comment.user_id == request.session['user_id']:
            comment.delete()
            return Response({}, status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        if comment.user_id == request.session['user_id']:
            data = JSONParser().parse(request)
            comment = Comment.objects.update(
                comment=comment, text=data['content'])
            comment.save()
            return Response({}, status=HTTP_204_NO_CONTENT)

    return Response({}, status=HTTP_400_BAD_REQUEST)
