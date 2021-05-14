from __future__ import division

import sys

from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import redirect
from tensorflow.python.data.experimental.ops.optimization import model

from .models import Photo
import tensorflow as tf
import tfjs_graph_converter
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths
import numpy as np


def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/list.html', {'photos': photos})


def ratio_get(request):
    if request.method == 'GET':
        ratio = request.GET['ratio']
    data = {
        'data': ratio,
    }
    return render(request, 'photo/realtime.html', ratio)


def ratio_calculate(array, height, width):
    array = list(array)
    # print(array)

    position = 0

    for i in array:
        if i == 40:
            first_face = position / width
            break
        position += 1

    position = 0
    for i in reversed(array):
        if i == 40:
            last_face = (len(array) - position) / width
            break
        position += 1

    position = 0
    for i in reversed(array):
        if i == 214:
            last_foot = (len(array) - position) / width
            break
        position += 1

    print("ff: ", first_face, "lf: ", last_face, "lf: ", last_foot)
    ratio = (abs(first_face - last_face) / abs(first_face - last_foot))

    return ratio


class PhotoUploadView(CreateView):
    model = Photo
    fields = ['photo']
    template_name = 'photo/upload.html'

    def form_valid(self, form):
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form': form})


class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete.html'

