
from rfsee import ClientProcess
from .example_stimxml import example_stim_xml

def main(): 
    
    cp = ClientProcess('rfsee_server')
    
    cp.config_stimulus_xml(example_stim_xml)
    
    # 10x slower
    # cp.config_compute_mu(True)
    
    position = [0.5, 0.5, 0.5]
    attitude = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    linear_velocity_body = [0, 0, 0]
    angular_velocity_body = [0, 0, 0]
    
    res = cp.render(position, attitude, linear_velocity_body, angular_velocity_body)
    
    print res['luminance']
    
    cp.close()


if __name__ == '__main__':
    main()
