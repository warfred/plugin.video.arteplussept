import os
import urllib2

def delete(file):
    if os.path.isfile(file):
        try:
            os.remove(file)
            return [ ( True ), ( 'OK' )  ]
        except OSError as e:
            return [ ( False ), ( e.strerror ) ]
    
    return [ ( True ), ( 'NOF' ) ]


def download_http( dest_file, src_url ):
    block_sz = 8192
    try:
       f = open(dest_file, 'wb')
    except IOError as e:
       return [ ( False ), ( e.strerror ) ]

    try:
        u = urllib2.urlopen(src_url)
        while True:
            buff = u.read(block_sz)
            if not buff:
                break
            f.write(buff)
        f.close()
    except IOError as e:
        return [ ( False ), ( e.strerror ) ]

    return [ ( True ), ( 'OK' ) ]
