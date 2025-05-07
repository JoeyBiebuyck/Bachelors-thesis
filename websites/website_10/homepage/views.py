from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
import random
#from run_atlucb_xss import n_arms

# n_arms = 13
# disarm_rate = 0.50
strongestDisarmedInput = 10

def homepage(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def search_view(request):
    query = request.GET.get('q', '')  # Get the search term from the URL

    # What to do with a specific query, eg. sampling from a binomial distribution and returning success or failure
    # could also do the below filtering by putting a < in the if clause
    # strongestDisarmedInput = int(n_arms * disarm_rate)
    disarmedInputs = [str(x) for x in list(range(1, strongestDisarmedInput+1))] # the weakest 50% (10) of the XSS payloads get sanitized by this website's filter (there are 20 transformations possible)

    # returning succes/failure
    if query in disarmedInputs:
        return HttpResponse(status=404) # query unsuccessfully attempted to evade XSS-filter
    else:
        return HttpResponse(status=200) # query successfully evaded XSS-filter

    # return render(request, 'search.html', {'query': query}) # uncomment this if you are manually testing whether an evasion technique works