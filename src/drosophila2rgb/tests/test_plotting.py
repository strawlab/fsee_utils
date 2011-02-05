import numpy as np
from PIL import Image
from drosophila2rgb import ommatidia2image, ommatidia2rgb, ommatidia2array


def ommatidia2array_test():
    bg = 10000
    N = 1398
    x = np.array(range(N))
    y = ommatidia2array(x, bg)
    
    xu = np.array(sorted(np.unique(x)))
    yu = np.array(sorted(np.unique(y)))
    
    assert yu[-1] == bg

    for i in range(N):
        if not i in yu:
            print('Warning: ommatidium %d not present in output.' % i)
    
    # np.testing.assert_allclose(xu, yu[:-1], atol=1e-5)

def ommatidia2image_test():
    N = 1398
    
    x = np.random.rand(N)
    
    ommatidia2image(x, 'ommatidia2image.png')
    ommatidia2image(x, 'ommatidia2image_bg.png', background=[200,0,0])
    ommatidia2image(x, 'ommatidia2image_reflines.png', add_reflines=True)


if __name__ == '__main__':
    ommatidia2array_test()
    ommatidia2image_test()