from django.http import JsonResponse
from django.shortcuts import render
import dml
import json
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId

"""
incomplete
"""

@csrf_exempt
def requestResponse(request):
    print("receive request")
    #json_str = ((request.body).decode('utf-8'))
    #rank = float(json.loads(json_str)['data'])
    min_rank = float(request.POST.get("min"))
    max_rank = float(request.POST.get("max"))
    if max_rank < min_rank:
        return sonResponse({'res':[]})
    client = dml.pymongo.MongoClient()
    repo = client.repo
    repo.authenticate('aolzh', 'aolzh')
    house_cluster = repo.aolzh.Cluster
    if min_rank != 0.0 and max_rank != 0:
        temp = []
        while min_rank <= max_rank:
            houses = house_cluster.find({'rank':min_rank})
            for h in houses:
                h['_id'] = 0
                temp.append({'data':h})
            min_rank+=0.5
    else:
        temp = []
        for i in range(10):
            houses = house_cluster.find({'cluster':i})
            for h in houses:
                h['_id'] = 0
                temp.append({'data':h})
    print(temp)
    return JsonResponse({'res':temp})