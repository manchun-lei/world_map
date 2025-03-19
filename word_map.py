# -*- coding: utf-8 -*-
"""
@author: Manchun LEI
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.lines import Line2D
from pyproj import Proj, transform
from geopy.distance import geodesic

import os
_path = os.path.dirname(os.path.abspath(__file__))
shapefile = os.path.join(_path,'ne_10m_admin_0_countries','ne_10m_admin_0_countries.shp')
world = gpd.read_file(shapefile)

def boundary_size_lonlat_to_meter(area):
    lon0,lat0,lon1,lat1 = area
    width0 = geodesic((lat0,lon0),(lat0,lon1)).meters
    width1 = geodesic((lat1,lon0),(lat1,lon1)).meters
    
    height = geodesic((lat0,lon0),(lat1,lon0)).meters
    return width0,width1,height

def lon_formatter(value,pos=None):
    if value < 0:
        return f"{abs(value):.0f}°W"
    else:
        return f"{value:.0f}°E"

def lat_formatter(value,pos=None):
    if value < 0:
        return f"{abs(value):.0f}°S"
    else:
        return f"{value:.0f}°N"

def lon_formatter_minute(value, pos=None):
    degrees = int(value)
    minutes = int(abs(value - degrees) * 60)
    if value < 0:
        return f"{abs(degrees):d}°{minutes:d}'W"
    else:
        return f"{degrees:d}°{minutes:d}'E"

def lat_formatter_minute(value, pos=None):
    degrees = int(value)
    minutes = int(abs(value - degrees) * 60)
    if value < 0:
        return f"{abs(degrees):d}°{minutes:d}'S"
    else:
        return f"{degrees:d}°{minutes:d}'N"

# def calculate_figure_dimensions(area_width, area_height, figure_height, margin_ratio=0.15):
#     aspect_ratio = area_width / area_height
#     figure_width = figure_height * aspect_ratio * (1 + margin_ratio)
#     return figure_width

def add_scalebar_x(ax, pos, area, scalebar_length_km, color="white",fontsize=10):
    x_pos,y_pos = pos
    width_meters0, width_meters1, height_meters = boundary_size_lonlat_to_meter(area)
    #计算比例尺在figure中的相对长度
    scalebar_length = scalebar_length_km * 1000 / width_meters0
    
    # 绘制比例尺的横线
    line = Line2D([x_pos,x_pos+scalebar_length], [y_pos,y_pos], transform=ax.transAxes, color=color, linewidth=2)
    ax.add_line(line)

    # 绘制比例尺两端的竖线
    side_bar = Line2D([x_pos,x_pos], [y_pos,y_pos+0.01], transform=ax.transAxes, color=color, linewidth=2)
    ax.add_line(side_bar)
    side_bar = Line2D([x_pos+scalebar_length,x_pos+scalebar_length], [y_pos,y_pos+0.01], transform=ax.transAxes, color=color, linewidth=2)
    ax.add_line(side_bar)

    # 在比例尺上方标注长度
    ax.text(
        x_pos + scalebar_length / 2, y_pos + 0.02, f"{scalebar_length_km} km",transform=ax.transAxes,
        horizontalalignment="center", verticalalignment="bottom", color=color, fontsize=fontsize
    )
    return ax

def word_map_lonlat(area, sub_area=None, dstfile=None, figure_height=8, fontsize=14):
    """
    Add red rec for sub_area if not None
    """
    lon0, lat0, lon1, lat1 = area
    area_width = lon1 - lon0
    area_height = lat1 - lat0
    
    aspect_ratio = area_width / area_height
    figure_width = figure_height * aspect_ratio

    #print('Dimension:',area_width,area_height)
    #print('Figure dimension:',figure_width,figure_height)

    clipped_world = world.cx[lon0:lon1, lat0:lat1]

    fig, ax = plt.subplots(figsize=(figure_width, figure_height))
    clipped_world.plot(ax=ax, color='lightgrey', edgecolor='black')

    if sub_area is not None:
        sub_lon0, sub_lat0, sub_lon1, sub_lat1 = sub_area
        rect = Rectangle(
            (sub_lon0, sub_lat0),
            abs(sub_lon1 - sub_lon0),
            abs(sub_lat1 - sub_lat0),
            linewidth=1,
            edgecolor='red',
            facecolor='none'
        )
        ax.add_patch(rect)

    ax.set_xlim(lon0, lon1)
    ax.set_ylim(lat0, lat1)
    ax.xaxis.set_major_formatter(FuncFormatter(lon_formatter))
    ax.yaxis.set_major_formatter(FuncFormatter(lat_formatter))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.tick_params(axis='both', labelsize=fontsize)
    # ax.set_xlabel("Longitude")
    # ax.set_ylabel("Latitude")

    plt.grid(color="gray", linestyle="--", linewidth=1)
    plt.tight_layout()
    if dstfile is not None:
        plt.savefig(dstfile, dpi=150, bbox_inches='tight')
    return fig, ax

def image_with_lonlat(srcfile,area,dstfile=None,figure_height=8,fontsize=12):

    lon0, lat0, lon1, lat1 = area
    img = mpimg.imread(srcfile)
    
    img_height, img_width = img.shape[:2]
    aspect_ratio = img_width / img_height
    figure_width = figure_height * aspect_ratio

    fig, ax = plt.subplots(figsize=(figure_width, figure_height))
    ax.imshow(img, extent=(lon0, lon1, lat0, lat1), aspect='auto')
    
    ax.xaxis.set_major_formatter(FuncFormatter(lon_formatter_minute))
    ax.yaxis.set_major_formatter(FuncFormatter(lat_formatter_minute))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.set_xlim(lon0, lon1)
    ax.set_ylim(lat0, lat1)
    ax.grid(color="gray", linestyle="--", linewidth=1)
    # ax.set_xlabel("Longitude")
    # ax.set_ylabel("Latitude")
    ax.tick_params(axis='both', labelsize=fontsize)
    plt.tight_layout()
    if dstfile:
        plt.savefig(dstfile, dpi=300, bbox_inches="tight")

    return fig,ax
    # plt.show()