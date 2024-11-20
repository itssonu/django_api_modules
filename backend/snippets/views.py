from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .models import Snippet
from.serializers import SnippetSerializer

@api_view(['GET'])
def snippetList(request):
    snippets = Snippet.objects.all()
    serializer = SnippetSerializer(snippets, many=True)
    return Response({
                'status': 'success',
                'data': serializer.data,
                'message': 'Snippets fetched successfully'
            }, status=status.HTTP_200_OK)

@api_view(['POST'])
def storeSnippet(request):
    serializer = SnippetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'success',
            'data': serializer.data,
            'message': 'snippet created successfully'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def getSnippet(request, snipetId):
    snippet = Snippet.objects.get(pk=snipetId)
    serializer = SnippetSerializer(snippet)
    return Response({
                'status': 'success',
                'data': serializer.data,
                'message': 'Snippets fetched successfully'
            }, status=status.HTTP_200_OK)

@api_view(['PUT'])
def updateSnippet(request, snipetId):
    snippet = Snippet.objects.get(pk=snipetId)
    serializer = SnippetSerializer(snippet, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'success',
            'data': serializer.data,
            'message': 'snippet updated successfully'
        }, status=status.HTTP_201_CREATED)
    
@api_view(['DELETE'])
def deleteSnippet(request, snipetId):
    snippet = Snippet.objects.get(pk=snipetId)
    serializer = SnippetSerializer(snippet)
    snippet.delete()
    return Response({
                'status': 'success',
                'data': serializer.data,
                'message': 'Snippets deleted successfully'
            }, status=status.HTTP_200_OK)
