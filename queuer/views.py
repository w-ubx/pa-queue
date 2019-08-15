from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Queue

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
