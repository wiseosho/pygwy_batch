import gwyutils, gwy, gc
from copy import deepcopy
from os import listdir, mkdir, getcwd
from os.path import isfile, join, isdir
import os, datetime
import re, shutil, imp
import numpy as np
if not '/home/june/.gwyddion/pygwy/scripts' in sys.path:
	sys.path.append('/home/june/.gwyddion/pygwy/scripts')
import Fct_gwyfunctions as custgwy
imp.reload(custgwy)
#ratio for color range
ratio = (0.05, 0.99)

pngexp = '/home/june/Dropbox/AFMImages'
cwd = '/home/june/LabServer/24HC/Images/SS-Canvas/SSC(T)/151108'
root = '/home/june/LabServer/24HC/Images/SS-Canvas/SSC(T)/151108'
cwd = '/home/june/LabServer/08JY/Exp.Data/sscanvas-GB/origami-1/20140511'
root = '/home/june/LabServer/08JY/Exp.Data/sscanvas-GB/origami-1/20140511'
def runbatch(root, cwd, pdr, pngexp, ratio):
    print(cwd)
    # Export PNG with scalebar
    s = gwy.gwy_app_settings_get()
    s['/module/pixmap/title_type'] = 0
    s['/module/pixmap/ztype'] = 0
    s['/module/pixmap/xytype'] = 0
    s['/module/pixmap/draw_maskkey'] = False
    # ... (*lots* of possible settings, see ~/.gwyddion/settings)

    Files_To_Open = [ f for f in listdir(cwd) if isfile(join(cwd,f)) ]
    
    print(Files_To_Open)
    if len(Files_To_Open) == 0:
        return 'No files'
    try:
        mkdir(join(cwd,'Processed'))
    except Exception as sym:
        print ('Already Exist')
        Tobe_Saved = join(cwd, 'Processed')
        filename_save = cwd.split('/')[-1]
        print (Files_To_Open)
    #Load first file to use as Merged file
    for filename in Files_To_Open:
        if not filename[-3:][-1].isdigit():
            Files_To_Open.remove(filename)
            continue
            
        print(filename)
        try:
            Temp = gwy.gwy_file_load(join(cwd,filename), RUN_NONINTERACTIVE)
            print(type(Temp))
            if type(Temp) == gwy.Container :
                print('right type')
                Cont_Dest = Temp
                Files_To_Open.remove(filename)
                Fstfilename = filename
                break
            Files_To_Open.remove(filename)
            print('loadedbutnot')
        except Exception as sym:
            print('except')
            print ("not proper file"+str(sym)+"\n")
            continue
        #Add into current browser and Make Visible on display
    try:
        gwy.gwy_app_data_browser_add(Cont_Dest)
    except Exception as ex:
        print(ex.args)
        return 'no veeco files to load'
    Cont_Dest.set_boolean_by_name('/0/data/visible', 1)
    print (Files_To_Open)
    #File Merge
    #First Container
    DataFields = gwyutils.get_data_fields_dir(Cont_Dest)
    for key in DataFields.keys():
        title = Cont_Dest.get_string_by_name(key+"/title")
        if (title == 'Amplitude') : Cont_Dest.remove_by_prefix('/'+key.split('/')[1]+'/')
        Cont_Dest.set_string_by_name(key+'/title', title+'.'+Fstfilename)

	#Rest of Containers
    print ('Rest of Files',Files_To_Open)
    for filename in Files_To_Open :
        if not filename[-3:][-1].isdigit():
            Files_To_Open.remove(filename)
            continue
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
    try:
        gwy_app_data_browser_remove(Cont_Source)
        del Cont_Source
        print (gc.collect())
    except Exception as ex:
        print (ex.args)
        
    try:
        mkdir(join(pngexp, root.split('/')[-1]))
    except :
        pass

    meta = open(join(pngexp, root.split('/')[-1])+'/'+'meta_file.txt' , 'a')
	#Change Palette, Flatten, Correct line, Remove Scars, Change Scale
    DataFields = gwyutils.get_data_fields_dir(Cont_Dest)
    for key in DataFields.keys():
        ID = key.split('/')[1]
        title = Cont_Dest.get_string_by_name(key+"/title")
        print (title+'\n')
        # Subtract polynomial background
        coeffs = DataFields[key].fit_polynom(3, 3)
        DataFields[key].subtract_polynom(3, 3, coeffs)
        DataFields[key].data_changed()
        #Get X Y scale
        si = {'x' : 'um' , 'y' : 'um'}
        size_x = DataFields[key].get_xreal()*1000000
        if (size_x < 1.0):
            size_x = size_x * 1000
            si['x'] = 'nm'
        size_y = DataFields[key].get_yreal()*1000000
        if (size_y < 1.0):
            size_y = size_y * 1000
            si['y'] = 'nm'
        scale = str(size_x)+si['x']+'by'+str(size_y)+si['y']
        title = title + '_'+ scale
        # Line and scar correction (run module functions)
        gwy.gwy_app_data_browser_select_data_field(Cont_Dest, int(ID))
        gwy.gwy_process_func_run("line_correct_median", Cont_Dest, gwy.RUN_IMMEDIATE)
        gwy.gwy_process_func_run("scars_remove", Cont_Dest, gwy.RUN_IMMEDIATE)
        gwy.gwy_process_func_run("fix_zero", Cont_Dest, gwy.RUN_IMMEDIATE)
        #Get Color Type
        colorr = Cont_Dest.get_int32_by_name('/'+ID+'/base/range-type')
        #Change_Color Palette
        Cont_Dest.set_string_by_name('/'+ID+'/base/palette', 'Gold')
        #Get Height Distribution and get Percentile color set range
        #Get CDH
        histogram = gwy.DataLine(1, 1, False)
        DataFields[key].dh(histogram, 512)
        median = histogram.get_max()
        data = histogram.get_data()
        ind_med = [i for i,v in enumerate(data) if data[i] == median][0]
        #Get Percentile Range	
        cumhistogram = gwy.DataLine(1, 1, False)
        DataFields[key].cdh(cumhistogram, 512)
        data = cumhistogram.get_data()
        Data_Range = DataFields[key].get_min_max()
        Hist_pct = [0, 0]
        Hist_pct[0] =  [float(index)/512 for index in range(ind_med, 0, -1) if (data[index] >= ratio[0] and data[index-1] <= ratio[0])][0]
        Hist_pct[1] =  [float(index)/512 for index in range(ind_med, 512, 1)  if (data[index] <= ratio[1] and data[index+1] >= ratio[1])][0]
        Range = Data_Range[1]-Data_Range[0]
        Color_Range = {'min': Data_Range[0]+Range*Hist_pct[0], 'max':Data_Range[0]+Range*Hist_pct[1]}
        Cont_Dest.set_boolean_by_name('/'+ID+'/data/visible', 1)
        Cont_Dest.set_int32_by_name('/'+ID+'/base/range-type' , 1)
        Cont_Dest.set_double_by_name('/'+ID+'/base/min', Color_Range['min'])
        Cont_Dest.set_double_by_name('/'+ID+'/base/max', Color_Range['max'])
        meta.write('Filename : '+ cwd+ '/' +str(title.split('Height.')[1])+'\n')
        meta.write('ColorRange : '+'{min : \t%e,\t max : \t%e }\n' %(Color_Range['min'] ,Color_Range['max']))
        #Change Color Range into (Full:0, Manual:1, Auto:2, Adaptive:3)
        #Cont_Dest.set_int32_by_name('/'+ID+'/base/range-type', 2)
        print (title)
        
        gwy.gwy_file_save(Cont_Dest, join(pngexp, root.split('/')[-1])+ '/' +str(title)+'%d.png' % int(ID), gwy.RUN_NONINTERACTIVE)
        Cont_Dest.set_boolean_by_name('/'+ID+'/data/visible', 0)
    try:
        gwy.gwy_file_save(Cont_Dest,join(cwd, 'Processed')+'/'+root.split('/')[-1]+pdr+'.gwy', gwy.RUN_NONINTERACTIVE)
    except Exception as ex:
        print(ex.args)
    gwy_app_data_browser_remove(Cont_Dest)
    del Cont_Dest
    print (gc.collect())
    meta.close()

def scan_dir_runbatch(root, cwd, pdr, pngexp, ratio):
	
    #####Go into the deepest folder
    dirs = [ f for f in listdir(cwd) if isdir(join(cwd,f)) ]
    try:
        dirs.remove('Processed')
    except :
        pass
    #dirs = {'./' : Files}
    for dr in dirs:
        scan_dir_runbatch(root, join(cwd, dr), dr, pngexp, ratio)
    runbatch(root, cwd, pdr, pngexp, ratio)
##########Get list of sub directories and run recursive self function

#custgwy.sep_files(root, cwd, 'DDX - postexp')

scan_dir_runbatch(root, cwd, cwd.split('/')[-1], pngexp, ratio)
