import gwyutils

def write_to_file(dataline, filename):
   # write content of dataline to specified file
   f = open(filename, "w")
   data = line.get_data()
   for num in data:
      f.write(str(num)+"\n")
   f.close()


# get active container
c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
# get filename of active container
filename = c.get_string_by_name("/filename")
# remove extension from filename
filebase = filename[0:-4]
# call 'level' process module as interactive
gwy.gwy_process_func_run("level", c, gwy.RUN_INTERACTIVE)
# call 'remove scars' process module
gwy.gwy_process_func_run("scars_remove", c, gwy.RUN_IMMEDIATE)

# set colors of first datafield in active container
c.set_string_by_name("/0/base/palette", "Green")

# save fixed file
gwy.gwy_file_save(c, filebase+"_fixed.gwy", gwy.RUN_NONINTERACTIVE)

# export datafield from container c specified by name to png file
gwyutils.save_dfield_to_png(c, "/0/data", filebase+"_fixed.png", gwy.RUN_INTERACTIVE)

# get active datafield
d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)

# create dataline for storing results of following methods
line = gwy.DataLine(1, 1, True)

# Calculate one-dimensional autocorrelation function of a data field.
d.hhcf(line, gwy.ORIENTATION_HORIZONTAL, gwy.INTERPOLATION_LINEAR, -1)
# write values to file
write_to_file(line, filebase+"_hhcf.txt")

# Calculates one-dimensional power spectrum density function of a data field.
d.psdf(line, gwy.ORIENTATION_HORIZONTAL, gwy.INTERPOLATION_LINEAR, gwy.WINDOWING_HANN, -1)
# write values to file
write_to_file(line, filebase+"_psdf.txt")

# Calculates distribution of heights in a data field.
d.dh(line, -1)
# write values to file
write_to_file(line, filebase+"_dh.txt")

# Computes basic statistical quantities of a data field.
avg, ra, rms, skew, kurtosis = d.get_stats()
# Save statistical quantities to file
f = open(filebase+"_stat.txt", "w")
f.write("avg "+str(avg) +"\nra "+str(ra)+"\nrms "+str(rms)+"\nskew "\
+str(skew)+"\nkurtosis "+ str(kurtosis))

# close file
f.close()

