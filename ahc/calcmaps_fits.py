import numpy as np
import os, sys
from astropy.io import fits 
from datetime import timedelta

sys.path.append('/Users/abdurrouf/Research/github_cook/AHC/ahc/')

from ahc import sunmoon as sm
from ahc import crescent as cs

if len(sys.argv) != 2:
	print ('# USAGE: python calcmaps_fits.py (1) Hijri year')
	sys.exit()

hijri_year = float(sys.argv[1])

hijri_months = sm.list_hijri_months()

factor = 1.0
min_lat1, max_lat1, min_long1, max_long1 = -90, 90, -180, 180
min_lat, max_lat, min_long, max_long = -60, 60, -180, 180

nlat = int(factor*((max_lat1-min_lat1)+1))
nlong = int(factor*((max_long1-min_long1)+1))
grid_lat = np.linspace(min_lat1, max_lat1, nlat)
grid_long = np.linspace(min_long1, max_long1, nlong)

nmonths = 12

# initiate FITS file production
hdul = fits.HDUList()
hdr = fits.Header()
hdr['software'] = 'AHC'
hdr['creator'] = 'Abdurrouf'
hdr['hijri_yy'] = int(hijri_year)
hdr['nlayers'] = 12
hdr['layer0'] = 'moon_alt_d1'
hdr['layer1'] = 'moon_arcv_d1'
hdr['layer2'] = 'moon_elong_d1'
hdr['layer3'] = 'moon_elong_geo_d1'
hdr['layer4'] = 'moon_width_d1'
hdr['layer5'] = 'moon_age_utc_seconds_d1' 

hdr['layer6'] = 'moon_alt_d2'
hdr['layer7'] = 'moon_arcv_d2'
hdr['layer8'] = 'moon_elong_d2'
hdr['layer9'] = 'moon_elong_geo_d2'
hdr['layer10'] = 'moon_width_d2'
hdr['layer11'] = 'moon_age_utc_seconds_d2'

hdr['minlat'], hdr['maxlat'] = -90, 90
hdr['minlong'], hdr['maxlong'] = -180, 180
hdr['minlat1'], hdr['maxlat1'] = -60, 60
hdr['minlong1'], hdr['maxlong1'] = -180, 180
hdr['nlat'] = nlat
hdr['nlong'] = nlong
primary_hdu = fits.PrimaryHDU(header=hdr)
hdul.append(primary_hdu)

for mm in range(int(nmonths)):
	# get conjuction UTC time
	ijtima_utc = sm.newmoon_hijri_month_utc(hijri_year, mm+1)

	hdr = fits.Header()
	hdr['conj_yy'] = ijtima_utc.year 
	hdr['conj_mm'] = ijtima_utc.month
	hdr['conj_dd'] = ijtima_utc.day 
	hdr['conj_h'] = ijtima_utc.hour
	hdr['conj_m'] = ijtima_utc.minute
	hdr['conj_s'] = ijtima_utc.second

	hdr['calc_yy1'] = ijtima_utc.year
	hdr['calc_mm1'] = ijtima_utc.month 
	hdr['calc_dd1'] = ijtima_utc.day 

	hdr['calc_yy2'] = ijtima_utc.year
	hdr['calc_mm2'] = ijtima_utc.month 
	hdr['calc_dd2'] = ijtima_utc.day + 1

	# get maps
	map_moon_alt = np.zeros((nlat,nlong))
	map_moon_arcv = np.zeros((nlat,nlong))
	map_moon_elong = np.zeros((nlat,nlong))
	map_moon_elong_geo = np.zeros((nlat,nlong))
	map_moon_width = np.zeros((nlat,nlong))
	map_moon_age_utc_seconds = np.zeros((nlat,nlong))
	#count = 0
	for yy in range(0,nlat-1):
		for xx in range(0,nlong-1):
			if grid_lat[yy]>=min_lat and grid_lat[yy]<=max_lat and grid_long[xx]>=min_long and grid_long[xx]<=max_long:
				lat1 = 0.5*(grid_lat[yy] + grid_lat[yy+1])
				long1 = 0.5*(grid_long[xx] + grid_long[xx+1])
				location = sm.set_location(lat1, long1, 0)
				sunrise, sunset = sm.sunrise_sunset_utc(location, year=ijtima_utc.year, month=ijtima_utc.month, day=ijtima_utc.day)
				if sunset is None:
					moon_alt, moon_arcv, moon_elong, moon_elong_geo, moon_width, moon_age_utc_seconds = float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')
				else:
					moon_alt, moon_az, dist = sm.moon_position_time_utc(location, utc_datetime=sunset)
					sun_alt, sun_az, dist = sm.sun_position_time_utc(location, utc_datetime=sunset)
					moon_arcv = moon_alt - sun_alt
					moon_elong = sm.moon_elongation_time_utc(location=location, utc_datetime=sunset)
					moon_elong_geo = sm.moon_elongation_time_utc(utc_datetime=sunset)
					illumination, moon_width, parallax, SD = sm.moon_illumination_width_utc(location=location, utc_datetime=sunset)
					moon_age_utc_delta = sunset - ijtima_utc
					moon_age_utc_seconds = moon_age_utc_delta.seconds

				map_moon_alt[yy][xx] = moon_alt
				map_moon_arcv[yy][xx] = moon_arcv
				map_moon_elong[yy][xx] = moon_elong
				map_moon_elong_geo[yy][xx] = moon_elong_geo
				map_moon_width[yy][xx] = moon_width
				map_moon_age_utc_seconds[yy][xx] = moon_age_utc_seconds
			else:
				map_moon_alt[yy][xx] = float('nan')
				map_moon_arcv[yy][xx] = float('nan')
				map_moon_elong[yy][xx] = float('nan')
				map_moon_elong_geo[yy][xx] = float('nan')
				map_moon_width[yy][xx] = float('nan')
				map_moon_age_utc_seconds[yy][xx] = float('nan')

			#count = count + 1
			#sys.stdout.write('\r')
			#sys.stdout.write('progress: month:%d --> %d of %d (%d%%)' % (mm+1,count,nlat*nlong,count*100/nlong/nlat))
			#sys.stdout.flush()

	map_moon_alt1 = np.zeros((nlat,nlong))
	map_moon_arcv1 = np.zeros((nlat,nlong))
	map_moon_elong1 = np.zeros((nlat,nlong))
	map_moon_elong_geo1 = np.zeros((nlat,nlong))
	map_moon_width1 = np.zeros((nlat,nlong))
	map_moon_age_utc_seconds1 = np.zeros((nlat,nlong))
	#count = 0
	for yy in range(0,nlat-1):
		for xx in range(0,nlong-1):
			if grid_lat[yy]>=min_lat and grid_lat[yy]<=max_lat and grid_long[xx]>=min_long and grid_long[xx]<=max_long:
				lat1 = 0.5*(grid_lat[yy] + grid_lat[yy+1])
				long1 = 0.5*(grid_long[xx] + grid_long[xx+1])
				location = sm.set_location(lat1, long1, 0)

				ijtima_utc_plus1 = ijtima_utc + timedelta(days=1)
				sunrise, sunset = sm.sunrise_sunset_utc(location, year=ijtima_utc_plus1.year, month=ijtima_utc_plus1.month, day=ijtima_utc_plus1.day)   ##############

				if sunset is None:
					moon_alt, moon_arcv, moon_elong, moon_elong_geo, moon_width, moon_age_utc_seconds = float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), float('nan')
				else:
					moon_alt, moon_az, dist = sm.moon_position_time_utc(location, utc_datetime=sunset)
					sun_alt, sun_az, dist = sm.sun_position_time_utc(location, utc_datetime=sunset)
					moon_arcv = moon_alt - sun_alt
					moon_elong = sm.moon_elongation_time_utc(location=location, utc_datetime=sunset)
					moon_elong_geo = sm.moon_elongation_time_utc(utc_datetime=sunset)
					illumination, moon_width, parallax, SD = sm.moon_illumination_width_utc(location=location, utc_datetime=sunset)
					moon_age_utc_delta = sunset - ijtima_utc
					moon_age_utc_seconds = moon_age_utc_delta.seconds

				map_moon_alt1[yy][xx] = moon_alt
				map_moon_arcv1[yy][xx] = moon_arcv
				map_moon_elong1[yy][xx] = moon_elong
				map_moon_elong_geo1[yy][xx] = moon_elong_geo
				map_moon_width1[yy][xx] = moon_width
				map_moon_age_utc_seconds1[yy][xx] = moon_age_utc_seconds
			else:
				map_moon_alt1[yy][xx] = float('nan')
				map_moon_arcv1[yy][xx] = float('nan')
				map_moon_elong1[yy][xx] = float('nan')
				map_moon_elong_geo1[yy][xx] = float('nan')
				map_moon_width1[yy][xx] = float('nan')
				map_moon_age_utc_seconds1[yy][xx] = float('nan')

			#count = count + 1
			#sys.stdout.write('\r')
			#sys.stdout.write('progress: month:%d --> %d of %d (%d%%)' % (mm+1,count,nlat*nlong,count*100/nlong/nlat))
			#sys.stdout.flush()

	# merge maps
	merge_map = np.zeros((12,nlat,nlong))
	merge_map[0] = map_moon_alt
	merge_map[1] = map_moon_arcv
	merge_map[2] = map_moon_elong
	merge_map[3] = map_moon_elong_geo
	merge_map[4] = map_moon_width
	merge_map[5] = map_moon_age_utc_seconds

	merge_map[6] = map_moon_alt1
	merge_map[7] = map_moon_arcv1
	merge_map[8] = map_moon_elong1
	merge_map[9] = map_moon_elong_geo1
	merge_map[10] = map_moon_width1
	merge_map[11] = map_moon_age_utc_seconds1

	hdul.append(fits.ImageHDU(data=merge_map, header=hdr, name=hijri_months[mm]))

	# end of for mm: nmonths

name_out_fits = '%d.fits' % hijri_year
hdul.writeto(name_out_fits, overwrite=True)
#print ('Produced '+name_out_fits)




