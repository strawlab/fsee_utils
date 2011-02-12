# Author: Floris van Breugel

# first run make_windtunnel_osg.py to create the osg stimulus
# use osgviewer to check the osg file

import numpy as np

from rfsee import ClientProcess
from windtunnel_stimxml import windtunnel_osg

from PIL import Image
from drosophila2rgb import ommatidia2image, ommatidia2rgb, ommatidia2array


def main(): 
    
    cp = ClientProcess('rfsee_server')
    cp.config_stimulus_xml(windtunnel_osg)
    
    #directory = '/home/floris/src/fsee_utils/src/examples/'
    directory = ''
    name_base = 'ommatidia2image_reflines_'
    name_suffix = '.png'
    
    
    frames = 100
    
    for i in range(frames):
        position = [0.5*np.sin(i), 0.5*np.sin(i), 0.5]
        print position[0]
        attitude = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        linear_velocity_body = [0, 0, 0]
        angular_velocity_body = [0, 0, 0]
        
        res = cp.render(position, attitude, linear_velocity_body, angular_velocity_body)
        lum = res['luminance']
        
        number = str(i)
        while len(number) < len(str(frames)):
            number = '0' + number
        
        name = directory + name_base + number + name_suffix
        ommatidia2image(lum, name, add_reflines=True)
    
    cp.close()
    

if __name__ == '__main__':
    main()
