FSee utils
==========

This repo contains a series of utilities that make using FSee easier.

Contents:

flydra_osg  
  Functions for converting a flydra XML stimulus description in a .osg world that can be used by FSee. Used by rfsee.

rfsee       
  This is a wrapper to call FSee as another process or another host. This is sometimes needed for stability, as it is not possible to make FSee load different stimulus files in a reliable way. Once you have inter-process communication, it is easy to put the two processes on different computers. This is useful if you are not able to install FSee on your computer.
  
  The communication between the two processes is based on JSON messages. At some point I was using this to use FSee from Matlab.
  
drosophila2rgb
  This package contains a simple, fast function to obtain an RGB image from the ommatidia intensity values. It uses a precomputed map of which pixels belong to which photoreceptors.
