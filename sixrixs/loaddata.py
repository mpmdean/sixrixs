""" Methods for loading data.
This is separated for process1d and process2d in order to facilitate loading
data from different sources.
"""

import numpy as np
import matplotlib.pyplot as plt
import h5py

def get_array(header):
    """ Get the RIXS data array associated with a header
    N.B. Appropriate for small data (due to simplicity)
    Not great if dataset is very big
    
    
    Parameters
    -----------
    header : databroker._core.Header
        The header associated with the data
        
    Returns
    -----------
    array : np.array
        four dimentional array
        axes are: events, images/event, rows, columns
    """
    array = np.array([im for im in header.data('rixscam_image')]).astype(np.int32)
    return array

def array_to_images(array):
    """ Index the real images out of the array
    
    Parameters
    -----------
    array : numpy array
        4d data array
        
    Returns
    -----------
    imageL : np.array
        four dimentional array corresponding to the left chip.
    imageR : np.array
        four dimentional array corresponding to the right chip.
    """
    roi_L = np.s_[:,:,175:1609,17:1649]
    roi_R = np.s_[:,:,175:1609,3319:4951]
    return array[roi_L], array[roi_R]

def image_to_photon_events(image):
    """ Convert 2D image into photon_events

    Parameters
    -----------
    image : np.array
        2D image

    Returns
    -----------
    photon_events : np.array
        three column x, y, I photon locations and intensities
    """
    X, Y = np.meshgrid(np.arange(image.shape[1]) + 0.5, np.arange(image.shape[0]) + 0.5)
    return np.vstack((X.ravel(), Y.ravel(), image.ravel())).transpose()

def photon_events_to_image(photon_events):
    """ Convert photon_events into image. Opposite of image_to_photon_events"""
    x = photon_events[:,0]
    y = photon_events[:,1]
    I = photon_events[:,2]

    xind = (x-0.5).astype(int)
    yind = (y-0.5).astype(int)
    image = np.zeros((yind.max()+1, xind.max()+1))
    image[yind, xind] = I
    return image




def get_spectrum(filename):
    """ return spectrum as
    pixel intensity
    shape rows, 2

    .txt are compatible with np.loadtxt
    """
    if filename[-4:].lower() == '.txt':
        return np.loadtxt(filename)
    elif filename[-3:].lower() == '.h5':
        h5file = h5py.File(filename)
        I = h5file['entry']['analysis']['spectrum'].value
        h5file.close()
        return np.vstack((np.arange(len(I)), I, I)).transpose()
    else:
        raise Exception('wrong file extension')