from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from search import search

# Create your views here.
def say_hello(request):
    return  HttpResponse('Hello World')

def main(request):
    return render(request, 'main.html')

def search_detail(request):
    query = request.GET.get('q', '')
    if query == '':
        return JsonResponse([])
    else:
        return search.get_relevant_docs(query, 20)

