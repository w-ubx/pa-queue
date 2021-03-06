from django.shortcuts import render
import base64

from django.http import HttpResponse
from .models import Queue, Wallet, UserQueue
from face_recog.models import FaceData
from face_recog.utils import compare_photo
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User

import json

def listing(request):
    active_queues = Queue.objects.all()
    context = {
        'active_queues' : active_queues
    }
    return render(request, 'queuer/listing.html', context)


def detail(request, queue_id):
    inspected_queue = Queue.objects.get(pk=queue_id)
    context = {
        'inspected_queue' : inspected_queue
    }
    return render(request, 'queuer/detail.html', context)


def increment(request):
    queue_id = request.POST['queue_id']
    inspected_queue = Queue.objects.get(pk=queue_id)
    inspected_queue.get_next_in_line()
    inspected_queue.save()
    return HttpResponse(inspected_queue.current_number)


def compare_faces(request):
    queue = Queue.objects.get(name=request.POST['queue_name'])
    target = UserQueue.objects.get(queue=queue, number=queue.current_number)
    target_face = FaceData.objects.get(user=target.user)

    img_data = request.POST['image']
    format, imgstr = img_data.split(';base64,')
    img = base64.b64decode(imgstr)
    filename = '/tmp/%s' % 'target_face'
    with open(filename, 'wb') as f:
        f.write(img)

    result = compare_photo(target_face.encoded, filename)
    if result==True:
        queue.current_number += 1
        queue.save()

    return HttpResponse(result)


@csrf_exempt
def current_number(request, queue_id):
    inspected_queue = Queue.objects.get(pk=queue_id)

    return HttpResponse(inspected_queue.current_number)


@csrf_exempt
def get_wallet(request):
    user = User.objects.get(username=request.GET['user_id'])
    wallet = Wallet.objects.get(user=user)
    response = {'wallet_value': wallet.value}

    return HttpResponse(json.dumps(response), 'application/json')


@csrf_exempt
def get_queue(request, queue_id):
    user = User.objects.get(username=request.GET['user_id'])
    queue = Queue.objects.get(id=queue_id)
    user_queue, created = UserQueue.objects.get_or_create(
        user=user, queue=queue,
        defaults={
            'number': queue.latest_assigned + 1
        }
    )

    response = {'number': user_queue.number}
    return HttpResponse(json.dumps(response), 'application/json')


@csrf_exempt
def assign_number(request):
    queue_id = request.POST['queue_id']
    user = User.objects.get(username=request.POST['user_id'])
    wallet = Wallet.objects.get(user=user)

    queue = Queue.objects.get(id=queue_id)
    user_queue, created = UserQueue.objects.update_or_create(
        user=user, queue=queue,
        defaults={
            'number': queue.latest_assigned + 1
        }
    )

    queue.latest_assigned += 1
    queue.save()
    response = {}
    if wallet.value >= 3:
        wallet.payment()
        response['assigned_number'] = user_queue.number
        status = 201
    else:
        response['assigned_number'] = 0
        status = 400

    return HttpResponse(json.dumps(response), 'application/json', status=status)

    
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