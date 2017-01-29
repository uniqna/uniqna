# coding=utf-8

import os
import json

from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from trumbowyg import settings as _settings
from trumbowyg.forms import ImageForm


@csrf_exempt
@require_POST
def upload_image(request):
    if not request.is_ajax():
        return HttpResponse(status=400)    # bad request
    if not (request.user.is_active and request.user.is_staff):
        return HttpResponse(status=403)    # forbidden

    image_form = ImageForm(request.POST, request.FILES)
    if image_form.is_valid():
        image = image_form.cleaned_data['image']
        path = os.path.join(_settings.UPLOAD_PATH, image.name)
        real_path = default_storage.save(path, image)
        context = {'message': 'uploadSuccess', 'file': default_storage.url(real_path)}
    else:
        context = {'message': image_form.errors['image'][0]}

    return HttpResponse(json.dumps(context), content_type='application/json')
