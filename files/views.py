import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
import requests

import urllib.parse

# Create your views here.

def files(request, slug):

    d = 1

    res = requests.get('http://localhost:8000/eln?id=' + slug)

    filespath = 'I:\\Files\\'

    resdict = json.loads(res.text)
    
    

    fr = FileResponse(open(filespath + resdict['id'] + ".tmp",'rb'))

    fr['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(resdict['filename'].encode('utf8'))
    fr['X-Sendfile'] = urllib.parse.quote(resdict['filename'].encode('utf8'))


    return fr

    # return JsonResponse(json.loads(res.text))
    # return redirect('http://localhost:8000/el?id=' + slug)