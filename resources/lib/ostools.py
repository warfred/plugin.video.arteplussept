import os
import urllib

def delete(file):
    if os.path.isfile(file):
        try:
            os.remove(file)
            return [ ( True ), ( 'OK' )  ]
        except OSError as e:
            return [ ( False ), ( e.strerror ) ]
    
    return [ ( True ), ( 'NOF' ) ]


def download_http( src_file, dest_file ):
    block_sz = 8192                                         
    f = open(dest_file, 'wb')    
    u = urllib2.urlopen(src_file)                   
    while True:             
        buff = u.read(block_sz)
        if not buff:                                        
            break
        f.write(buff)
    f.close()     
