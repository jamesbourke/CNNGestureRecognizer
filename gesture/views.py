# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from PIL import Image

from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

from cnn.cnninterface import process_image


def render_image(request, valid_image=None):
    valid_image = "jamesb.png" if not valid_image else valid_image

    try:
        with open(valid_image, "rb") as f:
            img = process_image(valid_image)
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
