from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

def homepage(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def search_view(request):
    query = request.GET.get('q', '')  # Get the search term from the URL
    return render(request, 'search.html', {'query': query})