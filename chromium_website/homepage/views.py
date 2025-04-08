from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import random

def homepage(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def search_view(request):
    query = request.GET.get('q', '')  # Get the search term from the URL
    # TODO: here we can add code about what to do with a specific query, eg. sampling from a binomial distribution and returning success or failure

    # currently returning a random succes/failure
    if random.randint(0, 1) == 0:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)

    # return render(request, 'search.html', {'query': query}) # uncomment this if you are manually testing whether an evasion technique works