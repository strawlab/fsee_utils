import numpy 

# TODO: make this configurable

# We try to hide this from pydev
optics1 = __import__('drosophila2rgb.optics_640x240', fromlist=['dummy'])
pixelmap = optics1.pixelmap
optics2 = __import__('drosophila2rgb.optics_reflines_640x240', fromlist=['dummy'])
reflines = optics2.reflines

def ommatidia2array(values, background=numpy.NaN):    
    ''' 
        Converts an array of 1398 values representing the intensity
        detected by each ommatidium into a 240x640 array representing
        the intensity map over the retinal space.
    '''
    n = len(values)

    if n != 1398:
        raise Exception('Expected 1398 values, not %d.' % n)
    
    valuesp = numpy.ndarray(shape=(n + 1,), dtype=values.dtype)
    
    valuesp[0:n] = values
    valuesp[n] = background
    
    return valuesp[pixelmap]


def ommatidia2rgb(values, background=[128,128,128], add_reflines=False):
    ''' 
        Converts intensities to an RGB images. Assumes values are floats 
        in the range [0,1].  
        
    '''
    values = numpy.array(values)
    
    n = len(values)
    
    if n != 1398:
        raise Exception('Expected 1398 values, not %d.' % n)

    r = numpy.ndarray(shape=(n + 1), dtype='uint8')
    g = numpy.ndarray(shape=(n + 1), dtype='uint8')
    b = numpy.ndarray(shape=(n + 1), dtype='uint8')
    
    r[0:n] = values * 255
    g[0:n] = values * 255
    b[0:n] = values * 255

    # background color    
    r[n] = background[0]
    g[n] = background[1]
    b[n] = background[2]
    
    rgb = numpy.ndarray(shape=(pixelmap.shape[0], pixelmap.shape[1], 3), 
                        dtype='uint8')
    rgb[:, :, 0] = r[pixelmap]
    rgb[:, :, 1] = g[pixelmap]
    rgb[:, :, 2] = b[pixelmap]
    
    if add_reflines:
        ref = reflines[:,:,0]
        rgb[:,:,0] *= ref
        rgb[:,:,1] *= ref
        rgb[:,:,2] *= ref

    return rgb
 
def ommatidia2image(values, filename, background=[128,128,128], add_reflines=False):
    ''' Calls ommatidia2rgb and then PIL to write to a file. '''
    rgb = ommatidia2rgb(values, background=background, add_reflines=add_reflines)
    from  .pil_conversion import Image_from_array
    image = Image_from_array(rgb)
    image.save(filename)



