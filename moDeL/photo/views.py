from __future__ import division

import sys

from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView
from django.shortcuts import redirect

from .models import Photo



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

