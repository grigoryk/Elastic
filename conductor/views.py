from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.cache import cache

from models import *

import pickle
import json

def get_cache(key):
    return cache.get(key)

def set_cache(key, value):
    cache.set(key, value)

def add_to_cached_set(key, value):
    xs = get_cache(key)
    
    if type(xs) is list:
        xs.append(value)
    else:
        xs = [value]
    
    set_cache(key, xs)    
    return xs

def node_landing(request):
    return render_to_response('client.html', {
    }, context_instance=RequestContext(request))

def node_announce(request):
    client_id = request.GET.get('client_id')
    
    active_nodes = add_to_cached_set('active-nodes', client_id)

    return HttpResponse(json.dumps(active_nodes))
    