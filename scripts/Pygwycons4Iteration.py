import gwyutils, gwy
filename_save = "/home/june/pygwy/test.gwy"
#Get all list of Loaded Containers(Opened Files)
OpenedFiles_All = gwy.gwy_app_data_browser_get_containers()

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
	OpenedFile.set_string_by_name('/'+ID+'/base/palette', 'Gold')
	print (key, title)

gwy.gwy_file_save(OpenedFiles_All[0],"/home/june/pygwy/test%d.gwy" % i, gwy.RUN_NONINTERACTIVE)