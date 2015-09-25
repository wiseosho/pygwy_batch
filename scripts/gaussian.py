# Gauss filter size
size = 1.0
number_of_iteration = 21

# get current datafield
d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)

# filename for storing statistical values
filename = "gaussian_filter_stats.txt"
f = open(filename, "w")

for i in range(number_of_iteration):
  # create copy of original datafield
  to_filter = d.duplicate()
  # apply gaussian filter to copy of datafield
  to_filter.filter_gaussian(i*size)
  # collect RMS to file
  f.write("iteration %d rms %e\n" % (i, to_filter.get_rms()))
  # get histogram
  histogram = gwy.DataLine(1, 1, False)
  to_filter.dh(histogram, -1)
  # write histogram to file
  f.write("histogram: ")
  for v in histogram.get_data():
    f.write("%e \n" % v)
f.write("\n" )
f.close()