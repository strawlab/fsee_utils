''' Precomputes the pixel map. '''

import numpy

import cairo

from .fsee_cairo import draw_fly_optics, draw_reference_lines

def setup_surface(width, height):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(surface)
    cr.translate(width / 2, height / 2)
    # note the minus here
    cr.scale(-width / 2, height / 2)
    
    return surface, cr

def create_eye_map(width, height):
    surface, cr = setup_surface(width, height)
    cr.set_line_width(0.01)
    
    data = numpy.frombuffer(surface.get_data(), numpy.uint8)
    data.shape = (height, width, 4)

    n = 1398

    M = numpy.zeros((height, width), dtype='int')
    M[:, :] = n # out of the buffer
    
    for k in range(n):
        # draw only the k-th ommatidium
        values = numpy.zeros(shape=(n))
        values[k] = 1 
        
        # set everything to zero on the buffer
        data[:, :, 1] = 0
        # then draw it
        draw_fly_optics(cr, values, optics='buchner71')
        
        # find the pixels that were used
        z = numpy.squeeze(data[:, :, 1])
        used = z > 0
        i, j = numpy.nonzero(used)
        
        M[i, j] = k
        print  "%4d/%d %4d pixels" % (k, n, len(i))
    
    filename = 'optics_%sx%s.py' % (width, height)
    print "Writing to %s" % filename
    with open(filename, 'w') as f:
        f.write('# autogenerated file\n')
        write_readable(M, f, 'pixelmap')
        
def create_lines(width, height):
    surface, cr = setup_surface(width, height)

    data = numpy.frombuffer(surface.get_data(), numpy.uint8)
    data.shape = (height, width, 4)
    # transparent green
    data[:, :, 3] = 0
    data[:, :, 2] = 0
    data[:, :, 1] = 255
    data[:, :, 0] = 255

    cr.scale(-1, 1) # strange bug
    draw_reference_lines(cr)
    
    filename = 'optics_reflines_%sx%s.py' % (width, height)
    print "Writing to %s" % filename
    with open(filename, 'w') as f:
        f.write('# autogenerated file\n')
        write_readable(data, f, 'reflines')

def write_readable(x, f, varname):
    x = numpy.array(x)
    if x.ndim == 2:
        f.write('%s = []\n' % varname)
        for i in range(x.shape[0]):
            l = x[i, :].tolist()
            f.write('%s.append(%r)\n' % (varname, l))
        f.write('import numpy\n')
        f.write('%s = numpy.array(%s)\n' % (varname, varname))
    elif x.ndim == 3:
        slicesvar = '%s_slices' % varname
        f.write('%s = []\n' % slicesvar)
        for k in range(x.shape[2]):
            val = x[:, :, k].squeeze()
            slicevar = '%s%d' % (varname, k)
            write_readable(val, f, slicevar)
            f.write('%s.append(%s)\n' % (slicesvar, slicevar))
        
        f.write('%s = numpy.dstack(%s)\n' % (varname, slicesvar))
        
    else:
        raise Exception("Wrong shape %s" % str(x.shape))


if __name__ == '__main__':
    # width, height = 480, 240
    width, height = 640, 240
    create_lines(width, height)
    create_eye_map(width, height)
    