import gwyutils, gwy, gc
from os import listdir, mkdir, getcwd
from os.path import isfile, join
#cwd = '/home/june/바탕화면/5hr10t reexp'
#cwd = '/home/june/바탕화면/Pragati-R/R1/12-09-2013 R1 n R2'
cwd = '/home/june/pygwy/Ring'
Files_To_Open = [ f for f in listdir(cwd) if isfile(join(cwd,f)) ]
try:
	mkdir(join(cwd,'Processed'))

except Exception as sym:
	print ('Already Exist')
Tobe_Saved = join(cwd, 'Processed')
filename_save = cwd.split('/')[-1]
print 

# Export PNG with scalebar
s = gwy.gwy_app_settings_get()
s['/module/pixmap/title_type'] = 0
s['/module/pixmap/ztype'] = 0
s['/module/pixmap/xytype'] = 0
s['/module/pixmap/draw_maskkey'] = False
# ... (*lots* of possible settings, see ~/.gwyddion/settings)
print (Files_To_Open)
#Load first file to use as Merged file
for filename in Files_To_Open:
	print(filename)
	try:
		print('try')
		Temp = gwy.gwy_file_load(join(cwd,filename), RUN_NONINTERACTIVE)
		print(type(Temp))
		if type(Temp) == gwy.Container :
			print('right type')
			Cont_Dest = Temp
			Files_To_Open.remove(filename)
			print (loaded)
			break
		Files_To_Open.remove(filename)
		print('loadedbutnot')
	except Exception as sym:
		print('except')
		print ("not proper file"+str(sym)+"\n")
		continue


gwy.gwy_app_data_browser_add(Cont_Dest)
#Make Visible
Cont_Dest.set_boolean_by_name('/0/data/visible', 1)
print (Files_To_Open)
#File Merge
#First Container
DataFields = gwyutils.get_data_fields_dir(Cont_Dest)
for key in DataFields.keys():
	title = Cont_Dest.get_string_by_name(key+"/title")
	if (title == 'Amplitude') : Cont_Dest.remove_by_prefix('/'+key.split('/')[1]+'/')
	Cont_Dest.set_string_by_name(key+'/title', title+'.'+Files_To_Open[0])

#Rest of Containers
for filename in Files_To_Open :
	#print (orgfile, join(cwd,filename))
	try:
		Temp_Source = gwy.gwy_file_load(join(cwd,filename), RUN_NONINTERACTIVE)
		if type(Temp_Source) == gwy.Container:
			Cont_Source = Temp_Source
			pass
		else:
			continue
	except Exception as sym:
		print ("not proper file"+sym+"\n")
		continue
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
	print (gc.collect())
	
#Change Palette, Flatten, Correct line, Remove Scars, Change Scale
DataFields = gwyutils.get_data_fields_dir(Cont_Dest)
for key in DataFields.keys():
	ID = key.split('/')[1]
	title = Cont_Dest.get_string_by_name(key+"/title")
	print (title+'\n')
	#get histogram
	# filename for storing statistical values
	filename = "gaussian_filter_stats.txt"
	f = open(cwd+'/'+filename, "w")
	histogram = gwy.DataLine(1, 1, Flase)
	DataFields[key].dh(histogram, -1)
	for v in histogram.get_data():
		f.write("%e \n" % v)
	f.close
	#Get Color Type
	colorr = Cont_Dest.get_int32_by_name('/'+ID+'/base/range-type')
	#Change_Color Palette
	Cont_Dest.set_string_by_name('/'+ID+'/base/palette', 'Gold')
	#Change Color Range into (Full:0, Manual:1, Auto:2, Adaptive:3)
	Cont_Dest.set_int32_by_name('/'+ID+'/base/range-type', 2)
	print (title)
	gwy.gwy_file_save(Cont_Dest, Tobe_Saved+'/'+str(title)+'%d.png' % int(ID), gwy.RUN_NONINTERACTIVE)
	Cont_Dest.set_boolean_by_name('/'+ID+'/data/visible', 0)
gwy.gwy_file_save(Cont_Dest,Tobe_Saved+'/'+filename_save+'.gwy', gwy.RUN_NONINTERACTIVE)

	
