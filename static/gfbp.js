function getFileByParts(filename, idname, ssize){

    if (ssize > 1024 * 1024 * 1024 * 1.8) {
    
        arch(filename, idname, ssize)
        
    } else {
        
        var link = document.createElement('a');
        link.download = filename;
    
        var pos = 0;
    
        const part_size = 120000;
    
        var blobs = [];
    
        document.querySelector("#filesize").innerHTML = "Размер " + Math.floor(pos * 100 / ssize) + "%";
    
        var req = new XMLHttpRequest();

        var url = "../gfbp/";
        req.open("GET", url, true);
        req.responseType = "arraybuffer";
        req.setRequestHeader('id', idname);
        req.setRequestHeader('pos', pos);
    
        req.onreadystatechange = function () { // (3)
    
            if (this.readyState != 4) return;
    
            // button.innerHTML = 'Готово!';
    
            if (this.status != 200) {
    
                setTimeout(onError, 1000);
                // alert(this.status + ': ' + this.statusText);
    
            } else {
    
                blobs.push(req.response);
    
                if(req.response.byteLength < part_size){
        
                    link.href = URL.createObjectURL(new Blob(blobs, {type: "application/zip"}));
            
                    link.click();
                    
                    URL.revokeObjectURL(link.href);             
        
                    document.querySelector("#filesize").innerHTML = "Размер";
        
                }
                else{
    
                    pos = pos + part_size;
        
                    document.querySelector("#filesize").innerHTML = "Размер " + Math.floor(pos * 100 / ssize) + "%";
        
                    req.open("GET", url, true);
                    req.responseType = "arraybuffer";
                    req.setRequestHeader('id', idname);
                    req.setRequestHeader('pos', pos);
                        req.send();
        
                }
            
            }
    
        }
    
        req.send();
    
    }

 }

 function getFileByPartsDirPos(number, index, size, dir, file, pos, partSize, blobs, callback) {

    document.querySelector("#filesize").innerHTML = '' + (index + 1) + ' (' + (number) + ') ' + Math.floor(pos * 100 / size) + "%";
    
    var url = "../gfbpd/";

    fetch(url, { method: 'GET', headers: { dir, file, pos } })
        .then( response => {

            response.blob()
                .then( data => {

                    blobs.push(data)

                    if(data.size == partSize){
            
                        getFileByPartsDirPos(number, index, size, dir, file, pos + partSize, partSize, blobs, callback)

                    } else {

                        callback()

                    }



                } )

        })
    
 }

function getFileByPartsDir(dir, files, index, callback) {
    
    if (index < files.length) {
        
        const curFile = files[index]

        const partSize = 120000;
 
        const blobs = [];
    
        getFileByPartsDirPos(files.length, index, 1024 * 1024 * 1024, dir, curFile, 0, partSize, blobs, err => {

            if (err) {
                
                callback(err)

            } else {

                var link = document.createElement('a');
                link.download = curFile;

                link.href = URL.createObjectURL(new Blob(blobs, {type: "application/zip"}));
        
                link.click();
                
                URL.revokeObjectURL(link.href);             
    
                blobs.splice(0, blobs.length)

                getFileByPartsDir(dir, files, index + 1, callback)    
                
            }

        })

    } else {

        document.querySelector("#filesize").innerHTML = 'ending...';
    
        var url = "../deldir/";

        fetch(url, { method: 'GET', headers: { dir } }).then( response => {

            document.querySelector("#filesize").innerHTML = 'loaded';
        
            callback()

        } )
    
        
    }

}

function arch(filename, id, ssize) {
    
    document.querySelector("#filesize").innerHTML = "Compressing..."
    
    var url = "../arch/";

    fetch(url, { method: 'GET', headers: { id, filename } })
        .then( response => {

            response.json()
                .then(data => {

                    getFileByPartsDir(data.dirid, data.files, 0, err => {



                    })

                })

        })


}
