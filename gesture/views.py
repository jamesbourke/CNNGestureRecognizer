# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import json
import tempfile
from PIL import Image

from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from cnn import cnninterface


def render_image(request, valid_image=None):
    valid_image = "jamesb.png" if not valid_image else valid_image

    try:
        with open(valid_image, "rb") as f:
            img = cnninterface.process_image(valid_image)
            return HttpResponse(img, content_type="image/png")
    except IOError:
        red = Image.new('RGBA', (1, 1), (255, 0, 0, 0))
        response = HttpResponse(content_type="image/png")
        red.save(response, "PNG")
        return response


def upload_image(request):
    if request.method == 'POST' and request.FILES['image_file']:
        myfile = request.FILES['image_file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        return render_image(request, filename)
    return render(request, 'upload_image.html')


@csrf_exempt
def process_image(request):
    response_data = ""
    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        imgdata = base64.b64decode(payload['img_data'].split(',')[1])

        if imgdata:
            fn = tempfile.mkstemp(".png")[1]
            with open(fn, 'wb') as f:
                f.write(imgdata)

            with open(fn, "rb") as f:
                img = cnninterface.process_image(fn)
                response_data = base64.b64encode(img)

    return JsonResponse({
                    "img_data": "data:image/png;base64," + response_data
                })


def webcam(request):
    return render(request, 'webcam.html')
