import base64
from django.shortcuts import render
from django.core.files import File
from django.contrib.auth.models import User
from face_recog.models import FaceData


def register_face(request):
    if request.method == 'GET':
        return render(request, 'show_camera.html')

    elif request.method == 'POST':
        user = User.objects.get(username=request.POST['user'])
        m, created = FaceData.objects.update_or_create(user=user)
        img_data = request.POST['image']
        format, imgstr = img_data.split(';base64,')
        img = base64.b64decode(imgstr)
        filename = 'tmp/%d' % user.id
        with open(filename, 'wb') as f:
            f.write(img)

        m.save()
        m.encode_photo(filename)

        return render(request, 'show_camera.html')
