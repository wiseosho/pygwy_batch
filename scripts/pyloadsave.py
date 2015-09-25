import gwyutils, gwy, gc
from os import listdir, mkdir, getcwd
from os.path import isfile, join
cwd = '/home/june/pygwy/cont'
Files_To_Open = [ f for f in listdir(cwd) if isfile(join(cwd,f)) ]
#mkdir(join(cwd,'Processed'))
filename_save = getcwd().split('/')[-1]
# Export PNG with scalebar
s = gwy.gwy_app_settings_get()
s['/module/pixmap/title_type'] = 0
s['/module/pixmap/ztype'] = 0
s['/module/pixmap/xytype'] = 0
s['/module/pixmap/draw_maskkey'] = False
# ... (*lots* of possible settings, see ~/.gwyddion/settings)

#Load first file to use as Merged file
Cont_Dest = gwy.gwy_file_load(join(cwd,Files_To_Open[0]), RUN_NONINTERACTIVE)
gwy.gwy_app_data_browser_add(Cont_Dest)
#Make Visible
Cont_Dest.set_boolean_by_name('/0/data/visible', 1)

#File Merge
#First Container
DataFields = gwyutils.get_data_fields_dir(Cont_Dest)
for key in DataFields.keys():
	title = Cont_Dest.get_string_by_name(key+"/title")
	if (title == 'Amplitude') : Cont_Dest.remove_by_prefix('/'+key.split('/')[1]+'/')
	Cont_Dest.set_string_by_name(key+'/title', title+'.'+Files_To_Open[0])

#Rest of Containers
for filename in Files_To_Open[1:] :
	print (orgfile, join(cwd,filename))
	Cont_Source = gwy.gwy_file_load(join(cwd,filename), RUN_NONINTERACTIVE)
	DataFields = gwyutils.get_data_fields_dir(Cont_Source)
	for key in DataFields.keys():
		ID = key.split('/')[1]
		title = Cont_Source.get_string_by_name(key+"/title")
		if (title == 'Height') :
			Cont_Source.set_string_by_name(key+'/title', title+'.'+filename)
			gwy.gwy_app_data_browser_copy_channel(Cont_Source, int(ID), Cont_Dest)
			print (key, title)
	gwy_app_data_browser_remove(Cont_Source)
	del Cont_Source
	gc.collect()
	