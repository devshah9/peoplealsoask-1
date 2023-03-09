from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from main import mainScraper
from paa.models import KeyWordOfPaa
from .serializers import KeyWordOfPaaSerializer


@api_view(['GET'])
def searchUsingKeyWord(request):
    keyWord = request.GET.get('q', None)
    if keyWord:
        searchData = KeyWordOfPaa.objects.filter(
            Q(keyword__icontains=keyWord.upper()) | Q(keyword__icontains=keyWord.title()) | Q(
                keyword__icontains=keyWord.lower()))
        if searchData:
            serializer = KeyWordOfPaaSerializer(searchData, many=True)
            return Response({'msg': 'success', 'data': serializer.data})
        else:
            return Response({'msg': 'data not found!'})
    else:
        return Response({'msg': 'q is required!'})


@api_view(['POST'])
def scrappingApi(request):
    keyword = request.GET.get('q', None)
    try:
        quantity = int(request.GET.get('quantity', 0))
    except (Exception,):
        quantity = 0
    related = request.GET.get('related', 'on')
    pixabay = request.GET.get('pixabay', 'on')
    pexels = request.GET.get('pexels', 'on')
    unsplash = request.GET.get('unsplash', 'on')
    gmedia = request.GET.get('gmedia', 'on')
    youtube = request.GET.get('youtube', 'on')
    paa = request.GET.get('paa', 'on')
    serp = request.GET.get('serp', 'on')
    if all([keyword, quantity, related, pixabay, pexels, unsplash, gmedia, youtube, paa, serp]):
        keyWordList = list(keyword.split(","))
        keyword, related, pixabay, pexels, unsplash, gmedia, youtube, paa, serp = \
            [k == 'on' for k in [keyword, related, pixabay, pexels, unsplash, gmedia, youtube, paa, serp]]
        scrapData = mainScraper(keyWordList, quantity, related, pixabay, pexels, unsplash, gmedia, youtube, paa, serp)
        return Response(scrapData)
    else:
        if keyword is None:
            return Response({'msg': 'q is required!'})
        if quantity is None:
            return Response({'msg': 'quantity is required!'})
        if related is None:
            return Response({'msg': 'related is required!'})
        if pixabay is None:
            return Response({'msg': 'pixabay is required!'})
        if pexels is None:
            return Response({'msg': 'pexels is required!'})
        if unsplash is None:
            return Response({'msg': 'unsplash is required!'})
        if gmedia is None:
            return Response({'msg': 'gmedia is required!'})
        if youtube is None:
            return Response({'msg': 'youtube is required!'})
        if paa is None:
            return Response({'msg': 'paa is required!'})
        if serp is None:
            return Response({'msg': 'serp is required!'})
