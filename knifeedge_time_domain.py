#!/usr/bin/env python3


from numpy import array, diag, transpose
from matplotlib.pyplot import plot, scatter, show, subplots
from math import erf
from scipy.optimize import curve_fit


def center(x_list, x_0):
    return array([(x - x_0) for x in x_list])


def fit(x, w, P_0):
    ''' fit function for power
        x = x - x_0, w = beam width, B_0 = amplitude / largest power '''
    return [P_0*0.5*(1 + erf(i/w)) for i in x]


def curve_fitting(arr, peaks, w, p):
    ''' wasn't able to test this one'''
    start = [w, p]
    pars, cov = curve_fit(fit, arr[::-1], peaks, p0=start)
    errs = sqrt(diag(cov))
    print(transpose(errs))
    return 


def plot_raw_data(arr, values):
    subplots()[1].plot(arr, values, 'o', color='purple')
    show()
    return


def pull_values(lines):
    return {float(l.split('\t')[-1].strip()) for l in lines if ' ' not in l}


def scatter_plot(arr, values, peaks, color = 'red'):
    plot(arr, values, color = color)
    scatter(arr[::-1], peaks)
    show()
    return


def sqrt(n):
    return n**(1/2)


if __name__ == '__main__':

    # this needs to be changed for future uses with different filepaths
    FILE_PATH = '/home/solaire/kenny'

    # distance of knifeedge from beam
    z_coor = [17.2, 18, 19.2, 20.8, 22]

    x_coor = [x/2 for x in range(13*2)]
    
    # peak values
    peak_values = {z:list() for z in z_coor}
    
    # filepath to all files 
    filepath = FILE_PATH + '/z_' + str(z_coor[0]) + '/xcoor_'
    for x in x_coor: 
        values = pull_values(open(filepath + str(x) + '.txt', 'r').readlines())
        peak_values[z_coor[0]] = array([max(values) - min(values)])
    x_array = center(x_coor, 6.25)
    
    plot_raw_data(x_array[::-1], peak_values[z_coor[0]])
    
    Winit, Pinit = 1.5, 11 
    scatter_plot(x_array, fit(x_array, Winit, Pinit), peak_values[z_coor[0]])
    scatter_plot(
        x_array, fit(x_array, Winit, Pinit), 
        peak_values[z_coor[0]], color='purple')
    
    #curve_fitting(x_array, peak_values[z_coor[0]], Winit, Pinit)


