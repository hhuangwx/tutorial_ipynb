#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author: hhuang
# @Date:   03_May_2017
# @Email:  hhuangmeso@gmail.com
# @Last modified by:   hhuang
# @Last modified time: 03_May_2017

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import cmaps


def _read_gfs(dataset, varname):
    var = dataset.variables[varname]
    return var


def read_gfs_data(fname, level=500., axis_lim=None):
    dataset = netCDF4.Dataset(fname)
    if axis_lim is None:
        lon_min, lon_max = 80., 130.
        lat_min, lat_max = 15., 50.
    else:
        lon_min, lon_max, lat_min, lat_max = axis_lim

    lv_varname = 'lv_ISBL0'
    lon_varname = 'lon_0'
    lat_varname = 'lat_0'
    s_lv = level * 100.  # plot 500hPa temperature height and wind
    lv_var = _read_gfs(dataset, lv_varname)[:]
    lv_index = np.nonzero(lv_var == s_lv)[0][0]

    lon_var = _read_gfs(dataset, lon_varname)[:]
    lat_var = _read_gfs(dataset, lat_varname)[:]

    lon_min_index = np.where(lon_var >= lon_min)[0][0]
    lon_max_index = np.where(lon_var <= lon_max)[0][-1] + 1
    lat_min_index = np.where(lat_var >= lat_min)[0][-1] + 1
    lat_max_index = np.where(lat_var <= lat_max)[0][0]

    t_varname = 'TMP_P0_L100_GLL0'
    t_var = _read_gfs(dataset, t_varname)[
        lv_index, lat_max_index: lat_min_index,
        lon_min_index:lon_max_index] - 273.15
    time_str = _read_gfs(dataset, t_varname).initial_time

    u_varname = 'UGRD_P0_L100_GLL0'
    v_varname = 'VGRD_P0_L100_GLL0'
    u_var = _read_gfs(dataset, u_varname)[
        lv_index, lat_max_index: lat_min_index,
        lon_min_index:lon_max_index]
    v_var = _read_gfs(dataset, v_varname)[
        lv_index, lat_max_index: lat_min_index,
        lon_min_index:lon_max_index]

    hgt_varname = 'HGT_P0_L100_GLL0'
    hgt_var = _read_gfs(dataset, hgt_varname)[
        lv_index, lat_max_index: lat_min_index,
        lon_min_index:lon_max_index] / 10.

    lon_f, lat_f = np.meshgrid(lon_var, lat_var, indexing='xy')
    lon = lon_f[lat_max_index: lat_min_index,
                lon_min_index:lon_max_index]
    lat = lat_f[lat_max_index: lat_min_index,
                lon_min_index:lon_max_index]

    return time_str, lon, lat, t_var, hgt_var, u_var, v_var


def main():
    fname = '/Users/hhuang/Downloads/gfsanl_4_20160628_0000_000.nc'
    # fname = '/Users/hhuang/Downloads/fnl_20160628_00_00.grib2.nc'
    axis_lim = [80., 130., 15., 50.]
    level = 500.
    time_str, lon, lat, t_var, hgt_var, u_var, v_var = read_gfs_data(
        fname, level=level, axis_lim=axis_lim)

    t_min, t_max, t_step = -20., 8., 2.
    t_level = np.linspace(t_min, t_max, (t_max - t_min) / t_step + 1)

    h_min, h_max, h_step = 560, 592., 4
    h_level = np.linspace(h_min, h_max, (h_max - h_min) / h_step + 1)

    plt.figure(figsize=(10, 8))
    plt.title('%g' % level +
              ' hPa Synoptic Analysis with GSF Analysis Data\nUTC' + time_str)
    cf = plt.contourf(
        lon, lat, t_var, vmin=t_min, vmax=t_max,
        cmap=cmaps.WhiteBlueGreenYellowRed,
        levels=t_level)

    cb = plt.colorbar(cf, ax=plt.gca(), ticks=t_level)
    cb.set_label('$\mathrm{Temperature(^\circ C)}$')

    cs = plt.contour(lon, lat, hgt_var, colors='b', levels=h_level)
    plt.clabel(cs, cs.levels, fmt='%g', fontsize=6, inline_spacing=10)
    plt.barbs(lon[::5, ::5], lat[::5, ::5], u_var[::5, ::5], v_var[::5, ::5],
              length=5)
    plt.axis(axis_lim)
    plt.xlabel('$\mathrm{Longitude(^\circ E)}$')
    plt.ylabel('$\mathrm{Lattitude(^\circ N)}$')
    plt.show()
if __name__ == '__main__':
    main()
