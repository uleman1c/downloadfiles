function getFileByParts(filename, idname, ssize){

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
 
