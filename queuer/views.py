from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Queue, Wallet
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

import json

def listing(request):
    active_queues = Queue.objects.all()
    context = {
        'active_queues' : active_queues
    }
    return render(request, 'queuer/listing.html', context)

@csrf_exempt
def current_number(request, queue_id):
    inspected_queue = Queue.objects.get(pk=queue_id)

    return HttpResponse(inspected_queue.current_number)

def get_wallet(request):
    wallet = Wallet.objects.get(user=request.user)
    response = {'wallet_value': wallet.value}
    
    return HttpResponse(json.dumps(response), 'application/json')

def detail(request, queue_id):
    inspected_queue = Queue.objects.get(pk=queue_id)
    context = {
        'inspected_queue' : inspected_queue
    }
    return render(request, 'queuer/detail.html', context)

@csrf_exempt
def increment(request):
    queue_id = request.POST['queue_id']
    inspected_queue = Queue.objects.get(pk=queue_id)
    inspected_queue.get_next_in_line()
    inspected_queue.save()
    return HttpResponse(inspected_queue.current_number)

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = request.user
    user = authenticate(username=username, password=password)

    if not user:
        response = {'message': 'Invalid username/password', 'status':'error'}
        return HttpResponse(json.dumps(response), 'application/json')
    else:
        response = {'message': 'Login Success', 'status':'success'}
        return HttpResponse(json.dumps(response), 'application/json')