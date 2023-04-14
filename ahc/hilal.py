import numpy as np 
from skyfield import api
from skyfield import almanac
from datetime import datetime
from datetime import timedelta
from calendar import monthrange
from skyfield.units import Angle

ts = api.load.timescale()

from .sunmoon import *
from .crescent import *
from .plotting import *

__all__ = ["hilal", "list_hilal_visibility_criteria", "calc_map_odeh", "calc_map_mabims", "calc_map_wujudul_hilal", "calc_map_turkey", "calc_map_danjon"]


def list_hilal_visibility_criteria(print_list=False):
	hilal_criteria = ["MABIMS", "Odeh", "Wujudul Hilal", "Turkey", "Danjon"]
	if print_list == True:
		for ii in range(0,len(hilal_criteria)):
			print ('%d %s' % (ii+1,hilal_criteria[ii]))

	return hilal_criteria


def calc_map_odeh(map_moon_width, map_moon_arcv):
	map_moon_width1 = map_moon_width*60.0
	map_V_odeh = map_moon_arcv - (-0.1018*np.power(map_moon_width1,3) + 0.7319*np.power(map_moon_width1,2) - 6.3226*map_moon_width1 + 7.1651)
	dimy, dimx = map_V_odeh.shape[0], map_V_odeh.shape[1]

	map_data = np.zeros((dimy,dimx)) + float('nan')

	# zone A
	rows, cols = np.where(map_V_odeh>=5.65)
	map_data[rows,cols] = 1

	# zone B
	rows, cols = np.where((map_V_odeh>=2) & (map_V_odeh<5.65))
	map_data[rows,cols] = 2

	# zone C
	rows, cols = np.where((map_V_odeh>=-0.96) & (map_V_odeh<2.0))
	map_data[rows,cols] = 3

	# zone D
	rows, cols = np.where(map_V_odeh<-0.96)
	map_data[rows,cols] = 4

	return map_data

def calc_map_mabims(map_moon_elong_geo, map_moon_alt):
	dimy, dimx = map_moon_alt.shape[0], map_moon_alt.shape[1]
	map_data = np.zeros((dimy,dimx)) + float('nan')

	rows, cols = np.where((map_moon_alt>3.0) & (map_moon_elong_geo>6.4))
	map_data[rows,cols] = 0

	rows, cols = np.where((map_moon_alt<=3.0) | (map_moon_elong_geo<=6.4))
	map_data[rows,cols] = 1

	return map_data

def calc_map_wujudul_hilal(map_moon_alt):
	dimy, dimx = map_moon_alt.shape[0], map_moon_alt.shape[1]
	map_data = np.zeros((dimy,dimx)) + float('nan')

	rows, cols = np.where(map_moon_alt>=-0.2575)
	map_data[rows,cols] = 0

	rows, cols = np.where(map_moon_alt<-0.2575)
	map_data[rows,cols] = 1

	return map_data

def calc_map_turkey(map_moon_elong, map_moon_alt, map_moon_age_utc, ijtima_utc, delta_day=0):
	dimy, dimx = map_moon_alt.shape[0], map_moon_alt.shape[1]
	map_data = np.zeros((dimy,dimx)) + float('nan')

	rows, cols = np.where((map_moon_alt>5.0) & (map_moon_elong>8.0))
	map_data[rows,cols] = 0

	rows, cols = np.where((map_moon_alt<=5.0) | (map_moon_elong<=8.0))
	map_data[rows,cols] = 1

	# locate area where local sunset occur before midnight UTC
	map_utc_midnight = np.zeros((dimy,dimx)) + float('nan')

	ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
	t0 = ts.utc(ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day, 0)
	utc_midnight_plus1 = t0.utc_datetime()

	delt_seconds_until_midnight_utc = (utc_midnight_plus1 - ijtima_utc).seconds

	rows, cols = np.where(map_moon_age_utc<delt_seconds_until_midnight_utc)    # qualified the criteria
	map_utc_midnight[rows,cols] = 1

	# calculate fajr time in New zealand with criteria sun_alt=-20
	latitude = -41.286460
	longitude = 174.776236
	elevation = 13.0
	time_zone_str = 'Pacific/Auckland'
	loc_name = 'NEW ZEALAND Wellington'
	location = set_location(latitude, longitude, elevation)
	if delta_day == 0:
		fajr_utc_NZ = fajr_time_utc(location, year=ijtima_utc.year, month=ijtima_utc.month, day=ijtima_utc.day, temperature_C=10.0, pressure_mbar=1030.0, fajr_sun_altitude=-20.0)
	else:
		ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
		fajr_utc_NZ = fajr_time_utc(location, year=ijtima_utc_plus1.year, month=ijtima_utc_plus1.month, day=ijtima_utc_plus1.day, temperature_C=10.0, pressure_mbar=1030.0, fajr_sun_altitude=-20.0)

	return map_data, map_utc_midnight, fajr_utc_NZ

def calc_map_danjon(map_moon_elong):
	dimy, dimx = map_moon_elong.shape[0], map_moon_elong.shape[1]
	map_data = np.zeros((dimy,dimx)) + float('nan')

	rows, cols = np.where(map_moon_elong>7.0)
	map_data[rows,cols] = 0

	rows, cols = np.where(map_moon_elong<=7.0)
	map_data[rows,cols] = 1

	return map_data


class hilal:

	def __init__(self, hijri_year, hijri_month, calculate_maps=False, plus_1day=True, min_lat=-60.0, max_lat=60.0, min_long=-180.0, max_long=180.0, factor=0.5):

		self.hijri_year = hijri_year
		self.hijri_month = hijri_month
		self.plus_1day = plus_1day
		self.calculate_maps = calculate_maps

		global ijtima_utc
		ijtima_utc = newmoon_hijri_month_utc(hijri_year, hijri_month)

		if calculate_maps == True:
			global map_moon_properties
			map_moon_properties = get_map_moon_properties_atsunset(ijtima_utc.year, ijtima_utc.month, ijtima_utc.day, ijtima_utc, plus_1day=plus_1day, 
													min_lat=min_lat, max_lat=max_lat, min_long=min_long, max_long=max_long, factor=factor)

	def map_moon_altitude(self):
		if self.calculate_maps == True:
			plot_map_moon_alt(map_moon_properties['alt'], self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day)
			if self.plus_1day == True:
				ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
				plot_map_moon_alt(map_moon_properties['alt1'], self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day)

	def map_moon_sun_altitude_difference(self):
		if self.calculate_maps == True:
			plot_map_moon_arcv(map_moon_properties['arcv'], self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day)
			if self.plus_1day == True:
				ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
				plot_map_moon_arcv(map_moon_properties['arcv1'], self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day)

	def map_moon_elongation(self):
		if self.calculate_maps == True:
			plot_map_moon_elong(map_moon_properties['elong'], self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day)
			if self.plus_1day == True:
				ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
				plot_map_moon_elong(map_moon_properties['elong1'], self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day)

	def map_moon_geocentric_elongation(self):
		if self.calculate_maps == True:
			plot_map_moon_elong_geo(map_moon_properties['elong_geo'], self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day)
			if self.plus_1day == True:
				ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
				plot_map_moon_elong_geo(map_moon_properties['elong_geo1'], self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day)

	def map_moon_width(self):
		if self.calculate_maps == True:
			plot_map_moon_width(map_moon_properties['width'], self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day)
			if self.plus_1day == True:
				ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
				plot_map_moon_width(map_moon_properties['width1'], self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day)

	def map_moon_age_utc_localsunset(self):
		if self.calculate_maps == True:
			plot_map_moon_age_utc_localsunset(map_moon_properties['age_utc'], self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day)
			if self.plus_1day == True:
				ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
				plot_map_moon_age_utc_localsunset(map_moon_properties['age_utc1'], self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day)

	def map_hilal_visibility(self, criterion):
		if self.calculate_maps == True:
			if criterion=='MABIMS' or criterion==1:
				map_data = calc_map_mabims(map_moon_properties['elong_geo'], map_moon_properties['alt'])
				plot_visibility_map_mabims(map_data, self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day)
				if self.plus_1day == True:
					map_data = calc_map_mabims(map_moon_properties['elong_geo1'], map_moon_properties['alt1'])
					ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
					plot_visibility_map_mabims(map_data, self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day)

			elif criterion=='Odeh' or criterion==2:
				map_data = calc_map_odeh(map_moon_properties['width'], map_moon_properties['arcv'])
				plot_visibility_map_odeh(map_data, self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day)
				if self.plus_1day == True:
					map_data = calc_map_odeh(map_moon_properties['width1'], map_moon_properties['arcv1'])
					ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
					plot_visibility_map_odeh(map_data, self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day)

			elif criterion=='Wujudul Hilal' or criterion==3:
				map_data = calc_map_wujudul_hilal(map_moon_properties['alt'])
				plot_visibility_map_wujudul_hilal(map_data, self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day)
				if self.plus_1day == True:
					map_data = calc_map_wujudul_hilal(map_moon_properties['alt1'])
					ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
					plot_visibility_map_wujudul_hilal(map_data, self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day)

			elif criterion=='Turkey' or criterion==4:
				map_data, map_utc_midnight, fajr_utc_NZ = calc_map_turkey(map_moon_properties['elong'], map_moon_properties['alt'], map_moon_properties['age_utc'], ijtima_utc, delta_day=0)
				plot_visibility_map_turkey(map_data, self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day, map_utc_midnight, fajr_utc_NZ, ijtima_utc)
				if self.plus_1day == True:
					ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
					map_data, map_utc_midnight, fajr_utc_NZ = calc_map_turkey(map_moon_properties['elong1'], map_moon_properties['alt1'], map_moon_properties['age_utc1'], ijtima_utc, delta_day=1)
					plot_visibility_map_turkey(map_data, self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day, map_utc_midnight, fajr_utc_NZ, ijtima_utc)

			elif criterion=='Danjon' or criterion==5:
				map_data = calc_map_danjon(map_moon_properties['elong'])
				plot_visibility_map_danjon(map_data, self.hijri_year, self.hijri_month, ijtima_utc.year, ijtima_utc.month, ijtima_utc.day)
				if self.plus_1day == True:
					map_data = calc_map_danjon(map_moon_properties['elong'])
					ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
					plot_visibility_map_danjon(map_data, self.hijri_year, self.hijri_month, ijtima_utc_plus1.year, ijtima_utc_plus1.month, ijtima_utc_plus1.day)

	def calculate_hilal_data(self, latitude, longitude, elevation, time_zone_str, loc_name=None, 
					delta_day=0, temperature_C=10.0, pressure_mbar=1030.0, sun_radius_degrees=0.2665, moon_radius_degrees=0.2575):

		crescent_data(self.hijri_year, self.hijri_month, latitude, longitude, elevation, time_zone_str, loc_name=loc_name, delta_day=delta_day, 
					temperature_C=temperature_C, pressure_mbar=pressure_mbar, sun_radius_degrees=sun_radius_degrees, moon_radius_degrees=moon_radius_degrees)







