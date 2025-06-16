# -*- coding: utf-8 -*-
"""
@author: Manchun LEI
"""
from word_map import *

# area = [-5, 41, 10, 52] # [lon0,lat0,lon1,lat1], lon0<lon1, lat0<lat1
# sub_area = [1.7, 48.5, 2.8, 49] # or = None 
area = [55.126, -21.398, 55.9046, -20.8470]
sub_area = [55.2021, -21.1096, 55.2620, -21.053]

fig,ax = word_map_lonlat(area, sub_area=sub_area, dstfile=None, figure_height=8, fontsize=14)
pos = (0.2,0.05) # scale bar position in the figure
scale_bar_length_km = 10 # scale bar unit length in km
add_scalebar_x(ax, pos, area, scale_bar_length_km, color="black",fontsize=10)
plt.savefig('demo.png')
plt.show()