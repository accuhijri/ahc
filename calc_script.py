from ahc.hilal import hilal


if len(sys.argv) != 3:
	print ('#USAGE: python cals_script.py (1)Hijri year (3)hijri month')
	sys.exit()


# input the hijri year and month. 
# since we want to get crescent (i.e., hilal) visibility maps later, so we set calculate_maps=True
# plus_1day input agrument indicates that we want to also calculate the visibility maps for 1 day after the conjunction (i.e., new moon phase)

hijri_year = float(sys.argv[1])
hijri_month = float(sys.argv[2])        
calculate_maps = True 
plus_1day = True
hl = hilal(hijri_year=hijri_year, hijri_month=hijri_month, calculate_maps=calculate_maps, plus_1day=plus_1day)

hl.map_moon_altitude()
hl.map_moon_sun_altitude_difference()
hl.map_moon_elongation()
hl.map_moon_geocentric_elongation()
hl.map_moon_width()
hl.map_moon_age_utc_localsunset()

hl.map_hilal_visibility('MABIMS')
hl.map_hilal_visibility('Odeh')
hl.map_hilal_visibility('Turkey')
hl.map_hilal_visibility('Danjon')
hl.map_hilal_visibility('Wujudul Hilal')
hl.map_hilal_visibility('Ijtima Qobla Ghurub')