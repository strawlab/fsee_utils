# Copyright (C) 2005-2008 California Institute of Technology, All rights reserved
# Author: Floris van Breugel; uses functions written by Andrew Straw
import fsee.scenegen.primlib as primlib
import math
import fsee.scenegen.osgwriter as osgwriter
import numpy as np

# function to create walls in 3D given the 3D center and dimensions of the wall. The dimension list should always have one value equal to zero.
def arena_wall(center, dimensions, texture):

    if dimensions[0] == 0:
        normals = (1,0,0)
        vertices = [    [ center[0]+dimensions[0]/2., center[1]-dimensions[1]/2., center[2]-dimensions[2]/2.], 
                        [ center[0]+dimensions[0]/2., center[1]-dimensions[1]/2., center[2]+dimensions[2]/2.],
                        [ center[0]+dimensions[0]/2., center[1]+dimensions[1]/2., center[2]+dimensions[2]/2.],
                        [ center[0]+dimensions[0]/2., center[1]+dimensions[1]/2., center[2]-dimensions[2]/2.] ]
                                
    if dimensions[1] == 0:
        normals = (0,1,0)
        vertices = [    [ center[0]-dimensions[0]/2., center[1]+dimensions[1]/2., center[2]-dimensions[2]/2.],
                        [ center[0]-dimensions[0]/2., center[1]+dimensions[1]/2., center[2]+dimensions[2]/2.],
                        [ center[0]+dimensions[0]/2., center[1]+dimensions[1]/2., center[2]+dimensions[2]/2.],
                        [ center[0]+dimensions[0]/2., center[1]+dimensions[1]/2., center[2]-dimensions[2]/2.]   ]               
        
    if dimensions[2] == 0:
        normals = (0,0,1)
        vertices = [    [ center[0]-dimensions[0]/2., center[1]-dimensions[1]/2., center[2]+dimensions[2]/2.],
                        [ center[0]-dimensions[0]/2., center[1]+dimensions[1]/2., center[2]+dimensions[2]/2.],
                        [ center[0]+dimensions[0]/2., center[1]+dimensions[1]/2., center[2]+dimensions[2]/2.],
                        [ center[0]+dimensions[0]/2., center[1]-dimensions[1]/2., center[2]+dimensions[2]/2.] ]

    print dimensions
    print    
    print vertices
    
    floor = primlib.Prim()
    floor.texture_fname = texture
    count = 0
    quads = []
    
    floor.verts = vertices
    floor.normals = [normals for i in range(4)]

    floor.tex_coords.append([0, 0])
    floor.tex_coords.append([0, 1])
    floor.tex_coords.append([1, 1])
    floor.tex_coords.append([1, 0])
    
    # there might be some bloat here... but it works.
    quads.append([count, count + 1, count + 2, count + 3])
    count += 4
    
    floor.prim_sets = [primlib.Quads(quads)]
    return floor
    

    
# make windtunnel osg: 
geode = osgwriter.Geode(states=['GL_LIGHTING OFF'])



# make the 5 walls of the windtunnel:
checkerboard_texture = "windtunnel_checkerwall_scaled.jpg"

center = np.array( [0, .1524, 0] )
dimensions = np.array( [1, 0, .3048] )
wall1 = arena_wall( center, dimensions, checkerboard_texture )
geode.append(wall1.get_as_osg_geometry())

center = np.array( [0, -.1524, 0] )
dimensions = np.array( [1, 0, .3048] )
wall2 = arena_wall( center, dimensions, checkerboard_texture )
geode.append(wall2.get_as_osg_geometry())

center = np.array( [0, 0, -.1524] )
dimensions = np.array( [1, .3048, 0] )
floor = arena_wall( center, dimensions, checkerboard_texture )
geode.append(floor.get_as_osg_geometry())
    
center = np.array( [-.5, 0, 0] )
dimensions = np.array( [0, .3048, .3048] )
texture = 'black.png'
end1 = arena_wall( center, dimensions, texture )
geode.append(end1.get_as_osg_geometry())

center = np.array( [.5, 0, 0] )
dimensions = np.array( [0, .3048, .3048] )
texture = 'black.png'
end2 = arena_wall( center, dimensions, texture )
geode.append(end2.get_as_osg_geometry())

# make cylinder / post:
radius = .01
height = 0.2286
z0 = -.1524
z1 = height+z0
if 1:
    res = 72
    angles = np.linspace( 0.0, 360.0, res+1 )
    starts = angles[:-1]
    stops = angles[1:]

    D2R = math.pi/180.0
    start_x = radius*np.cos(starts*D2R)
    start_y = radius*np.sin(starts*D2R)
    stop_x = radius*np.cos(stops*D2R)
    stop_y = radius*np.sin(stops*D2R)

    for i in range(len(start_x)):
        x1 = start_x[i]; y1 = start_y[i]
        x2 = stop_x[i]; y2 = stop_y[i]

        wall = primlib.XZRect()
        if i%2==0:
            wall.texture_fname = 'black.png'
        else:
            wall.texture_fname = 'black.png'
        wall.mag_filter = "NEAREST"
        wall.verts = [[ x1, y1, z0],
                      [ x1, y1, z1],
                      [ x2, y2, z1],
                      [ x2, y2, z0]]
        geode.append(wall.get_as_osg_geometry())


m = osgwriter.MatrixTransform(np.eye(4))
m.append(geode)

g = osgwriter.Group()
g.append(m)

fd = open('windtunnel_test.osg','wb')
g.save(fd)
fd.close()






