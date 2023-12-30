import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
import requests

import urllib.parse

import py7zr
import multivolumefile

import uuid
import os

import shutil

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

def arch(request):

    filespath = 'I:\\Files\\'
    
    curUid = request.headers.get('id')
    
    target = filespath + curUid + ".tmp"

    diruuid = str(uuid.uuid4())

    os.mkdir(filespath + diruuid)
    
    filters = [{'id': py7zr.FILTER_COPY}]
    
    with multivolumefile.open(filespath + diruuid + '\\' + curUid + '.7z', mode='wb', volume=1024 * 1024 * 1024) as target_archive:
        with py7zr.SevenZipFile(target_archive, filters=filters, mode='w') as archive:
            archive.write(target)
    return JsonResponse( { 'dirid': diruuid, 'files': os.listdir(filespath + diruuid) } )


def deldir(request):

    filespath = 'I:\\Files\\'
    
    diruuid = request.headers.get('dir')
    
    shutil.rmtree(filespath + diruuid)

    # for file in os.listdir(filespath + diruuid):
    #     os.remove(filespath + diruuid + '\\' + file)
    
    # os.rmdir(diruuid)

    return JsonResponse( { 'success': True } ) 

def gfbpd(request):

    filespath = 'I:\\Files\\'
    
    curDirUid = request.headers.get('dir')
    curFile = request.headers.get('file')
    pos = int(request.headers.get('pos'))

    frf = open(filespath + curDirUid + '\\' + curFile, 'rb')

    frf.seek(pos)

    part_size = 120000

        # fr = FileResponse(frf.read(part_size))
        
        # fr['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(fo.name.encode('utf8'))
        # fr['X-Sendfile'] = urllib.parse.quote(fo.name.encode('utf8'))

    return HttpResponse(frf.read(part_size), content_type='application/octet-stream')

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

    
    