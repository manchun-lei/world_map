# -*- coding: utf-8 -*-
"""
@author: Manchun LEI
"""
from word_map import *

area = [-5, 41, 10, 52] # [lon0,lat0,lon1,lat1]
sub_area = [1.7, 48.5, 2.8, 49]
fig,ax = word_map_lonlat(area, sub_area=sub_area, dstfile=None, figure_height=8, fontsize=14)
add_scalebar_x(ax, (0.7,0.05), area, 100, color="black",fontsize=10)
plt.savefig('demo.png')
plt.show()