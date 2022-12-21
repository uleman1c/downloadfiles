import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
import requests

import urllib.parse

addr = 'http://localhost:8011/'

# Create your views here.

def files(request, slug):

    res = requests.get(addr + 'eln?id=' + slug)

    try:

        resdict = json.loads(res.text)
        
        filespath = 'I:\\Files\\'

        

        fr = FileResponse(open(filespath + resdict['id'] + ".tmp",'rb'))

        fr['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(resdict['filename'].encode('utf8'))
        fr['X-Sendfile'] = urllib.parse.quote(resdict['filename'].encode('utf8'))


        return fr

    except:
        
        return render(request, '404.html')

def filesd(request, slug, mode):

    res = requests.get(addr + 'eln?id=' + slug)

    try:

        resdict = json.loads(res.text)
        
        filespath = 'I:\\Files\\'

        return render(request, 'index.html', locals())

    except:
    
        return render(request, '404.html')


def gfbp(request):

    filespath = 'I:\\Files\\'
    
    curUid = request.headers.get('id')
    pos = int(request.headers.get('pos'))

    frf = open(filespath + curUid + ".tmp",'rb')

    frf.seek(pos)

    part_size = 120000

        # fr = FileResponse(frf.read(part_size))
        
        # fr['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(fo.name.encode('utf8'))
        # fr['X-Sendfile'] = urllib.parse.quote(fo.name.encode('utf8'))

    return HttpResponse(frf.read(part_size), content_type='application/octet-stream')

    
    