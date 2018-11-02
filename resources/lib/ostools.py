import os

def delete(file):
    if os.path.isfile(file):
        try:
            os.remove(file)
            return [ ( True ), ( 'OK' )  ]
        except OSError as e:
            return [ ( False ), ( e.strerror ) ]
    
    return [ ( True ), ( 'NOF' ) ]
