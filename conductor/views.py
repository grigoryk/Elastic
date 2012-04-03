from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import WebTask, KV
from utilities import *

import pickle
import json
import math
import base64
import random

def node_landing(request):
    return render_to_response('client.html', {
    }, context_instance=RequestContext(request))


def mark_node_active(client_id):
    set_cache('active-node-%s' % client_id, True, 3)
    active_nodes = add_to_cached_set('active-nodes', 'active-node-%s' % client_id, is_node=True)
    
    return active_nodes

def node_announce(request):
    client_id = request.GET.get('client_id')
    
    active_nodes = mark_node_active(client_id)

    return HttpResponse(json.dumps({"nodes": active_nodes}))

def split_items_between_nodes(nodes, items):
    per_node = math.ceil(float(len(items)) / float(len(nodes)))
    
    assignments = {}
    for i in range(0, len(nodes)):
        node = nodes[i]
        # overlap with 'next' node
        lower = i * per_node
        upper = i * per_node + per_node * 2
        
        if upper > len(items) - 1:
            items1 = items[int(lower):]
            items2 = items[:int(per_node)]
            curl = items1 + items2
        else:
            curl = items[int(i*per_node):int(upper)]    
        
        assignments[node] = curl
    
    return assignments

def node_getwork(request):
    TIME_TO_LIST_REMIX = 60
    TIME_TO_FINISH_MAP = 60
    
    client_id = request.GET.get('client_id')
    web_tasks = get_cache("web_tasks")
    if not web_tasks:
        web_tasks = WebTask.objects.filter(complete=False)
        set_cache("web_tasks", web_tasks, 60 * 2)
    
    try:
        # pick a random incomplete task
        task = random.choice(web_tasks)
    except:
        return HttpResponse(0)
    
    urls = pickle.loads(str(task.urls))
    nodes = mark_node_active(client_id)
    
    # get current url assignment, or remix the assignments based on new node list
    current_node_urls = get_cache("%s-active-node-%s" % (task.id, client_id))
    if not current_node_urls:
        url_assignments = split_items_between_nodes(nodes, urls)
        for node in url_assignments.keys():
            if client_id in node:
                current_node_urls = url_assignments[node]
        
            set_cache("%s-active-node-%s" % (task.id, node), url_assignments[node], TIME_TO_LIST_REMIX)
    
    if not current_node_urls:
        return HttpResponse(0)
    
    complete_map = True
    for url in current_node_urls:
        url_status = get_cache(url)
        
        # 'mapped' url
        if url_status == True:
            continue
        
        # unassigned url
        if url_status == None:
            set_cache(url, "active-node-%s" % client_id, TIME_TO_FINISH_MAP)
            return HttpResponse(json.dumps({"task_id": task.id, "url": url, "map": True}))
        
        # url assigned to another node which is currently 'mapping' it
        else:
            complete_map = False
            continue
    
    # all urls are now mapped
    if complete_map:
        # reduce
        current_node_reduce = get_cache("%s-active-node-%s-reduce" % (task.id, client_id))
        if not current_node_reduce:
            reduce_keys = get_cache("%s-keys" % task.id)
            reduce_assignments = split_items_between_nodes(nodes, reduce_keys)
            for node in reduce_assignments.keys():
                if client_id in node:
                    current_node_reduce = reduce_assignments[node]
                
                set_cache("%s-active-node-%s-reduce" % (task.id, client_id), reduce_assignments[node], TIME_TO_LIST_REMIX)
        
        complete_reduce = True
        for reduce_key in current_node_reduce:
            reduce_key_status = get_cache("%s-%s-results" % (task.id, reduce_key))
            
            # key assigned to another node
            if reduce_key_status == True and reduce_key_status != 1:
                complete_reduce = False
                continue
            
            # unassigned key
            elif reduce_key_status == None:
                set_cache("%s-%s-results" % (task.id, reduce_key), True, TIME_TO_FINISH_MAP)
                key_items = get_cache("%s-%s" % (task.id, reduce_key))
                print "%s-%s :: %s" % (task.id, reduce_key, key_items)
                return HttpResponse(json.dumps({"task_id": task.id, "key": reduce_key, "item_list": json.dumps(key_items), "reduce": True}))
            
            # 'reduced' key
            else:
                continue
        
        # job is complete!
        if complete_reduce:
            results = get_cache("%s-reduced" % task.id)
            task.results = pickle.dumps(results)
            task.complete = True
            task.save()
    
    # Nothing to do
    return HttpResponse(0)

def node_emit(request):
    TIME_TO_JOB_EXPIRE = 60 * 60 * 24
    phase = request.GET.get('phase')
    task_id = request.GET.get('task_id')
    key = request.GET.get('key')
    value = request.GET.get('val')
    url = request.GET.get('url')
    
    if key:
        key = key.replace("\r", "").replace("\n", "")
    
    if url:
        url = url.replace("%3F", "?").replace("%3D", "=").replace("%26", "&")
    
    # individual key emit
    if phase == "map" and key:
        add_to_cached_set("%s-keys" % task_id, key, TIME_TO_JOB_EXPIRE)
        add_to_cached_set("%s-%s" % (task_id, key), value, TIME_TO_JOB_EXPIRE)
    
    # finished mapping url
    elif phase == "map" and url:
        set_cache(url, True, TIME_TO_JOB_EXPIRE)
        
    elif phase == "reduce":
        set_cache("%s-%s-results" % (task_id, key), value, TIME_TO_JOB_EXPIRE)
        add_to_cached_set("%s-reduced" % task_id, (key, value), TIME_TO_JOB_EXPIRE)
    
    return HttpResponse(0)

def data_get(request):
    key = request.GET.get('key')
    split_from = request.GET.get('from')
    split_to = request.GET.get('to')
    
    chunk = get_cache('%s-%s-%s' % (key, split_from, split_to))
    
    return HttpResponse(chunk)

def task_map(request, task_id):
    url = request.GET.get('url')
    callback = request.GET.get('_')
    
    task = WebTask.objects.get(id=task_id)
    
    map_code = task.map_code
    map_code = map_code.replace("%task_id%", task_id)
    map_code = map_code.replace("%url%", url)
    return HttpResponse(map_code, mimetype='application/javascript')

def task_reduce(request, task_id):
    task = WebTask.objects.get(id=task_id)
    key = request.GET.get('key')
    item_list = request.GET.get('item_list')
    
    item_list = [int(x) for x in json.loads(item_list)]
    
    reduce_code = task.reduce_code
    reduce_code = reduce_code.replace("%task_id%", task_id)
    reduce_code = reduce_code.replace("%key%", key)
    reduce_code = reduce_code.replace("%item_list%", "%s" % item_list)
    
    return HttpResponse(reduce_code, mimetype='application/javascript')