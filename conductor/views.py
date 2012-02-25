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
    cache.set(key, value, 30)

def add_to_cached_set(key, value):
    xs = get_cache(key)
    
    if not xs:
        xs = []
    
    if value not in xs: 
        xs.append(value)
    
    set_cache(key, xs)
    return xs

def node_landing(request):
    return render_to_response('client.html', {
    }, context_instance=RequestContext(request))

def node_announce(request):
    client_id = request.GET.get('client_id')
    
    active_nodes = add_to_cached_set('active-nodes', client_id)

    return HttpResponse(json.dumps(active_nodes))

def node_getwork(request):
    web_tasks = WebTask.objects.filter(complete=False)
    
    if len(web_tasks) == 0:
        return HttpResponse(0)
    
    for task in web_tasks:
        all_urls = pickle.loads(web_tasks.urls)
        try:
            url = all_urls.pop()
            return HttpResponse(json.dumps({"url": url, "task_id": task.id}))
            
        except:
            continue
    
def node_emit(request):
    pass