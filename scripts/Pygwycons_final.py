import gwyutils, gwy
filename_save = "/home/june/pygwy/test.gwy"
#Get all list of Loaded Containers(Opened Files)
OpenedFiles_All = gwy.gwy_app_data_browser_get_containers()
# Export PNG with scalebar
s = gwy.gwy_app_settings_get()
s['/module/pixmap/title_type'] = 0
s['/module/pixmap/ztype'] = 0
s['/module/pixmap/xytype'] = 0
s['/module/pixmap/draw_maskkey'] = False
# ... (*lots* of possible settings, see ~/.gwyddion/settings)

#Get filename of the container & Datafield Titles
Filename = []
Filename = OpenedFiles_All[0].get_string_by_name('/filename').split('/')[-1]
#File Merge
#First Container
DataFields = gwyutils.get_data_fields_dir(OpenedFiles_All[0])
for key in DataFields.keys():
	title = OpenedFiles_All[0].get_string_by_name(key+"/title")
	if (title == 'Amplitude') : OpenedFiles_All[0].remove_by_prefix('/'+key.split('/')[1]+'/')
	OpenedFiles_All[0].set_string_by_name(key+'/title', title+'.'+Filename)
#Rest of Containers
for OpenedFile in OpenedFiles_All[1:]:
	Filename = OpenedFile.get_string_by_name('/filename').split('/')[-1]
	DataFields = gwyutils.get_data_fields_dir(OpenedFile)
	for key in DataFields.keys():
		ID = key.split('/')[1]
		title = OpenedFile.get_string_by_name(key+"/title")
		if (title == 'Height') :
			OpenedFile.set_string_by_name(key+'/title', title+'.'+Filename)
			gwy.gwy_app_data_browser_copy_channel(OpenedFile, int(ID), OpenedFiles_All[0])
			print (key, title)

#Change Palette, Flatten, Correct line, Remove Scars, Change Scale
OpenedFile = OpenedFiles_All[0]
DataFields = gwyutils.get_data_fields_dir(OpenedFile)
for key in DataFields.keys():
	ID = key.split('/')[1]
	title = OpenedFile.get_string_by_name(key+"/title")
	print (title+'\n')
	# Subtract polynomial background
	coeffs = DataFields[key].fit_polynom(3, 3)
	DataFields[key].subtract_polynom(3, 3, coeffs)
	DataFields[key].data_changed()
	# Line and scar correction (run module functions)
	gwy.gwy_app_data_browser_select_data_field(OpenedFile, int(ID))
	gwy.gwy_process_func_run("line_correct_median", OpenedFile, gwy.RUN_IMMEDIATE)
	gwy.gwy_process_func_run("scars_remove", OpenedFile, gwy.RUN_IMMEDIATE)
	gwy.gwy_process_func_run("fix_zero", OpenedFile, gwy.RUN_IMMEDIATE)
	#Get Color Type
	colorr = OpenedFile.get_int32_by_name('/'+ID+'/base/range-type')
	#Change_Color Palette
	OpenedFile.set_string_by_name('/'+ID+'/base/palette', 'Gold')
	#Change Color Range into (Full:0, Manual:1, Auto:2, Adaptive:3)
	OpenedFile.set_int32_by_name('/'+ID+'/base/range-type', 2)
	gwy.gwy_file_save(OpenedFile, '/home/june/pygwy/test%d.png' % int(ID), gwy.RUN_NONINTERACTIVE)
gwy.gwy_file_save(OpenedFiles_All[0],filename_save, gwy.RUN_NONINTERACTIVE)

