import numpy as np
import os, sys
import matplotlib.pyplot as plt
import geopandas
from matplotlib.ticker import StrMethodFormatter

from .sunmoon import *
from .crescent import *

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))


__all__ = ["plot_map_moon_alt", "plot_map_moon_arcv", "plot_map_moon_elong", "plot_map_moon_elong_geo", "plot_map_moon_width", "plot_map_moon_age_utc_localsunset", 
			"plot_visibility_map_odeh", "plot_visibility_map_wujudul_hilal", "plot_visibility_map_mabims", "plot_visibility_map_turkey", 
			"plot_visibility_map_danjon", "plot_visibility_map_IQG"]


def plot_map_moon_alt(map_moon_alt, hijri_year, hijri_month, yy, mm, dd):
	hijri_months = list_hijri_months()

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Moon altitude of %s %d \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(map_moon_alt, origin='lower', alpha=0.0, extent=[-180, 180, -90, 90], aspect='auto')

	x = np.linspace(-180, 180, map_moon_alt.shape[1])
	y = np.linspace(-90, 90, map_moon_alt.shape[0])
	X, Y = np.meshgrid(x, y)

	# define levels
	rows, cols = np.where(map_moon_alt > -10)
	levels = np.arange(int(np.percentile(map_moon_alt[rows,cols],5)), int(np.percentile(map_moon_alt[rows,cols],98)+1))

	CS = ax.contour(X, Y, map_moon_alt, colors='red', levels=levels)
	ax.clabel(CS, inline=True, fontsize=13, colors='blue', fmt='%.1f°')

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
						verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'moon_alt_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)


def plot_map_moon_arcv(map_moon_arcv, hijri_year, hijri_month, yy, mm, dd):
	hijri_months = list_hijri_months()

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Moon-Sun altitude difference (ARCV) of %s %d \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(map_moon_arcv, origin='lower', alpha=0.0, extent=[-180, 180, -90, 90], aspect='auto')

	x = np.linspace(-180, 180, map_moon_arcv.shape[1])
	y = np.linspace(-90, 90, map_moon_arcv.shape[0])
	X, Y = np.meshgrid(x, y)

	# define levels
	rows, cols = np.where(map_moon_arcv > -10)
	levels = np.arange(int(np.percentile(map_moon_arcv[rows,cols],5)), int(np.percentile(map_moon_arcv[rows,cols],98)+1))

	CS = ax.contour(X, Y, map_moon_arcv, colors='red', levels=levels)
	ax.clabel(CS, inline=True, fontsize=13, colors='blue', fmt='%.1f°')

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
						verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'moon_arcv_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)


def plot_map_moon_elong(map_moon_elong, hijri_year, hijri_month, yy, mm, dd):
	hijri_months = list_hijri_months()

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Moon topocentric elongation of %s %d \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(map_moon_elong, origin='lower', alpha=0.0, extent=[-180, 180, -90, 90], aspect='auto')

	x = np.linspace(-180, 180, map_moon_elong.shape[1])
	y = np.linspace(-90, 90, map_moon_elong.shape[0])
	X, Y = np.meshgrid(x, y)

	# define levels
	rows, cols = np.where(map_moon_elong > -10)
	levels = np.arange(int(np.percentile(map_moon_elong[rows,cols],5)), int(np.percentile(map_moon_elong[rows,cols],95)+1))

	CS = ax.contour(X, Y, map_moon_elong, colors='red', levels=levels)
	ax.clabel(CS, inline=True, fontsize=13, colors='blue', fmt='%.1f°')

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
						verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'moon_elong_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)


def plot_map_moon_elong_geo(map_moon_elong_geo, hijri_year, hijri_month, yy, mm, dd):
	hijri_months = list_hijri_months()

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Moon geocentric elongation of %s %d \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(map_moon_elong_geo, origin='lower', alpha=0.0, extent=[-180, 180, -90, 90], aspect='auto')

	x = np.linspace(-180, 180, map_moon_elong_geo.shape[1])
	y = np.linspace(-90, 90, map_moon_elong_geo.shape[0])
	X, Y = np.meshgrid(x, y)

	# define levels
	rows, cols = np.where(map_moon_elong_geo > -10)
	levels = np.arange(int(np.percentile(map_moon_elong_geo[rows,cols],5)), int(np.percentile(map_moon_elong_geo[rows,cols],98)+1))

	CS = ax.contour(X, Y, map_moon_elong_geo, colors='red', levels=levels)
	ax.clabel(CS, inline=True, fontsize=13, colors='blue', fmt='%.1f°')

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
						verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'moon_elong_geo_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)


def plot_map_moon_width(map_moon_width, hijri_year, hijri_month, yy, mm, dd):
	map_moon_width1 = map_moon_width*60.0
	hijri_months = list_hijri_months()

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Moon width of %s %d \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(map_moon_width1, origin='lower', alpha=0.0, extent=[-180, 180, -90, 90], aspect='auto')

	x = np.linspace(-180, 180, map_moon_width1.shape[1])
	y = np.linspace(-90, 90, map_moon_width1.shape[0])
	X, Y = np.meshgrid(x, y)

	# define levels
	rows, cols = np.where(map_moon_width1 > -10)
	levels = np.linspace(np.percentile(map_moon_width1[rows,cols],10), np.percentile(map_moon_width1[rows,cols],95), 10)

	CS = ax.contour(X, Y, map_moon_width1, colors='red', levels=levels)
	ax.clabel(CS, inline=True, fontsize=13, colors='blue', fmt='%.2f′')

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
						verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'moon_width_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)


def plot_map_moon_age_utc_localsunset(map_moon_age_utc0, hijri_year, hijri_month, yy, mm, dd):
	map_moon_age_utc = map_moon_age_utc0/3600

	hijri_months = list_hijri_months()

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Moon age UTC of %s %d \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(map_moon_age_utc, origin='lower', alpha=0.0, extent=[-180, 180, -90, 90], aspect='auto')

	x = np.linspace(-180, 180, map_moon_age_utc.shape[1])
	y = np.linspace(-90, 90, map_moon_age_utc.shape[0])
	X, Y = np.meshgrid(x, y)

	# define levels
	rows, cols = np.where(map_moon_age_utc > -10)
	levels = np.linspace(np.percentile(map_moon_age_utc[rows,cols],10), np.percentile(map_moon_age_utc[rows,cols],95), 10)

	CS = ax.contour(X, Y, map_moon_age_utc, colors='red', levels=levels)
	ax.clabel(CS, inline=True, fontsize=13, colors='blue', fmt='%.2f hours')

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
						verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'moon_age_utc_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)


def plot_visibility_map_odeh(data_map, hijri_year, hijri_month, yy, mm, dd):
	from matplotlib.colors import ListedColormap

	hijri_months = list_hijri_months()

	cmap = ListedColormap(["green", "magenta", "blue", "red"])

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Crescent visibility map of %s %d based on Odeh criterion \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(data_map, origin='lower', alpha=0.4, cmap=cmap, zorder=1, extent=[-180, 180, -90, 90], aspect='auto')
	#plt.colorbar()

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	ax.text(0.45, 0.05, "Naked eyes", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(0))

	ax.text(0.55, 0.05, "Optical aid, naked eye possible", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(1))

	ax.text(0.78, 0.05, "Optical aid only", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(2))

	ax.text(0.9, 0.05, "Not visible", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(3))

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'map_odeh_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)


def plot_visibility_map_mabims(data_map, hijri_year, hijri_month, yy, mm, dd):
	from matplotlib.colors import ListedColormap

	hijri_months = list_hijri_months()

	cmap = ListedColormap(["green", "red"])

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Crescent visibility map of %s %d based on MABIMS criterion \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(data_map, origin='lower', alpha=0.4, cmap=cmap, zorder=1, extent=[-180, 180, -90, 90], aspect='auto')
	#plt.colorbar()

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	ax.text(0.8, 0.045, "Visible", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(0))

	ax.text(0.9, 0.045, "Not visible", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(1))

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'map_mabims_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)


def plot_visibility_map_wujudul_hilal(data_map, hijri_year, hijri_month, yy, mm, dd):
	from matplotlib.colors import ListedColormap

	hijri_months = list_hijri_months()

	cmap = ListedColormap(["green", "red"])

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Crescent map of %s %d based on Wujudul Hilal criterion \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(data_map, origin='lower', alpha=0.4, cmap=cmap, zorder=1, extent=[-180, 180, -90, 90], aspect='auto')
	#plt.colorbar()

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	ax.text(0.8, 0.045, "Qualified", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(0))

	ax.text(0.9, 0.045, "Not qualified", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(1))

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'map_wh_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)


def plot_visibility_map_turkey(data_map, hijri_year, hijri_month, yy, mm, dd, map_utc_midnight, fajr_utc_NZ, ijtima_utc):
	from matplotlib.colors import ListedColormap

	hijri_months = list_hijri_months()

	cmap = ListedColormap(["green", "red"])

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Crescent visibility map of %s %d based on Turkey criterion \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(data_map, origin='lower', alpha=0.4, cmap=cmap, zorder=1, extent=[-180, 180, -90, 90], aspect='auto')
	ax.contourf(map_utc_midnight, 2, hatches=['xx', None], colors='none', alpha=0.0, extent=[-180, 180, -90, 90])

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	ax.text(0.38, 0.045, "New moon UTC: %d-%d-%d %02d:%02d:%02d" % (ijtima_utc.day,ijtima_utc.month,ijtima_utc.year,ijtima_utc.hour,ijtima_utc.minute,ijtima_utc.second), 
				horizontalalignment='left', fontweight='bold', verticalalignment='center', transform = ax.transAxes, fontsize=10, color='darkred')

	ax.text(0.38, 0.02, "Fajr NZ UTC: %d-%d-%d %02d:%02d:%02d" % (fajr_utc_NZ.day,fajr_utc_NZ.month,fajr_utc_NZ.year,fajr_utc_NZ.hour,fajr_utc_NZ.minute,fajr_utc_NZ.second), 
				horizontalalignment='left', fontweight='bold', verticalalignment='center', transform = ax.transAxes, fontsize=10, color='darkred')

	ax.text(0.62, 0.045, "Sunset before midnight UTC", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	ax.text(0.83, 0.045, "Visible", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(0))

	ax.text(0.9, 0.045, "Not visible", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(1))

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'map_turkey_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)


def plot_visibility_map_danjon(data_map, hijri_year, hijri_month, yy, mm, dd):
	from matplotlib.colors import ListedColormap

	hijri_months = list_hijri_months()

	cmap = ListedColormap(["green", "red"])

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title("Crescent visibility map of %s %d based on Danjon's limit \n Calculated at sunset time on %d-%d-%d" % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(data_map, origin='lower', alpha=0.4, cmap=cmap, zorder=1, extent=[-180, 180, -90, 90], aspect='auto')
	#plt.colorbar()

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	ax.text(0.8, 0.045, "Visible", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(0))

	ax.text(0.9, 0.045, "Not visible", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(1))

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'map_danjon_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)

def plot_visibility_map_IQG(data_map, hijri_year, hijri_month, yy, mm, dd):
	from matplotlib.colors import ListedColormap

	hijri_months = list_hijri_months()

	cmap = ListedColormap(["green", "red"])

	fig = plt.figure(figsize=(15,7))
	ax = plt.subplot()
	plt.title('Crescent map of %s %d based on Ijtima Qobla Ghurub \n Calculated at sunset time on %d-%d-%d' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy), fontsize=16)
	plt.ylim(-70,80)
	plt.xlim(-180+2,180-2)
	plt.setp(ax.get_xticklabels(), fontsize=13)
	plt.setp(ax.get_yticklabels(), fontsize=13)

	ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
	ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))

	plt.rc('grid', linestyle=':', color='red', linewidth=2)
	world.plot(ax=ax, color='lightgray', edgecolor='black', zorder=0)
	plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

	plt.imshow(data_map, origin='lower', alpha=0.4, cmap=cmap, zorder=1, extent=[-180, 180, -90, 90], aspect='auto')
	#plt.colorbar()

	ax.text(0.01, 0.03, "Accurate Hijri Calculator, by Abdurro'uf", horizontalalignment='left', fontname="Brush Script MT", 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color='black')

	ax.text(0.8, 0.045, "Qualified", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(0))

	ax.text(0.9, 0.045, "Not qualified", horizontalalignment='left', fontweight='bold', 
				verticalalignment='center', transform = ax.transAxes, fontsize=11, color=cmap(1))

	plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.9)

	name_plot = 'map_IQG_%s_%d_%d%d%d.png' % (hijri_months[int(hijri_month)-1],hijri_year,dd,mm,yy)
	plt.savefig(name_plot)






