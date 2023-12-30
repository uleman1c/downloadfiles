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

import threading

addr = 'http://localhost:8011/'

filespath = 'I:\\Files\\'
    

# Create your views here.

def files(request, slug):

    res = requests.get(addr + 'eln?id=' + slug)

    try:

        resdict = json.loads(res.text)
        
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
        
        return render(request, 'index.html', locals())

    except:
    
        return render(request, '404.html')


def archfile(diruuid, curUid, curName):

    target = filespath + curUid + ".tmp"

    filters = [{'id': py7zr.FILTER_COPY}]
    
    with multivolumefile.open(filespath + diruuid + '\\' + curUid + '.7z', mode='wb', volume=1024 * 1024 * 1024) as target_archive:
        with py7zr.SevenZipFile(target_archive, filters=filters, mode='w') as archive:
            archive.write(target, curName)

    os.remove(filespath + curUid + ".lck")

def extFileList(dir):

    fileList = os.listdir(filespath + dir)

    extFileList = list()
    
    for fi in fileList:

        #file_stats = os.stat(filespath + dir + '\\' + fi)

        fileSize = 0 # file_stats.st_size

        extFileList.append( { 'name': fi, 'size': fileSize } )

    return extFileList


def filearchived(request):

    curUid = request.headers.get('id')
    curDirUid = request.headers.get('dirid')

    lock = filespath + curUid + ".lck"

    return JsonResponse( { 'compressing': os.path.isfile(lock), 'dirid': curDirUid, 'files': extFileList(curDirUid) } )
    
def arch(request):

    curUid = request.headers.get('id')
    curName = request.headers.get('filename')
    
    lock = filespath + curUid + ".lck"

    isFileLocked = os.path.isfile(lock)

    if isFileLocked:

        lockFile = open(lock, 'r')

        diruuid = lockFile.readline()

    else:

        diruuid = str(uuid.uuid4())

        lockFile = open(lock, 'w')
        lockFile.write(diruuid)
        lockFile.close()

        os.mkdir(filespath + diruuid)
        
        thread = threading.Thread(target=archfile, args=(diruuid, curUid, curName))
        thread.start()        


    return JsonResponse( { 'compressing': True, 'dirid': diruuid, 'files': extFileList(diruuid) } )
#        return JsonResponse( { 'dirid': diruuid, 'files': os.listdir(filespath + diruuid) } )


def deldir(request):

    diruuid = request.headers.get('dir')
    
    shutil.rmtree(filespath + diruuid)

    # for file in os.listdir(filespath + diruuid):
    #     os.remove(filespath + diruuid + '\\' + file)
    
    # os.rmdir(diruuid)

    return JsonResponse( { 'success': True } ) 

def gfbpd(request):

    curDirUid = request.headers.get('dir')
    curFile =  urllib.parse.unquote(request.headers.get('file'), encoding='utf-8')
    pos = int(request.headers.get('pos'))

    frf = open(filespath + curDirUid + '\\' + curFile, 'rb')

    frf.seek(pos)

    part_size = 120000

        # fr = FileResponse(frf.read(part_size))
        
        # fr['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(fo.name.encode('utf8'))
        # fr['X-Sendfile'] = urllib.parse.quote(fo.name.encode('utf8'))

    return HttpResponse(frf.read(part_size), content_type='application/octet-stream')

def gfbp(request):

    curUid = request.headers.get('id')
    pos = int(request.headers.get('pos'))

    frf = open(filespath + curUid + ".tmp",'rb')

    frf.seek(pos)

    part_size = 120000

        # fr = FileResponse(frf.read(part_size))
        
        # fr['Content-Disposition'] = 'attachment; filename=' + urllib.parse.quote(fo.name.encode('utf8'))
        # fr['X-Sendfile'] = urllib.parse.quote(fo.name.encode('utf8'))

    return HttpResponse(frf.read(part_size), content_type='application/octet-stream')

    
    