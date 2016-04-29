# Gauss filter size
size = 1.0
number_of_iteration = 21
# get current datafield
d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
# filename for storing statistical values
filename = "gaussian_filter_stats.txt"
f = open(filename, "w")

# get histogram
histogram = gwy.DataLine(1, 1, False)
d.cdh(histogram, 512)
# write histogram to file
f.write("histogram: \n")
data = histogram.get_data()
for v in data:
	f.write("%e \n" % v)
f.write("\n" )
f.close()
ratio = (0.05, 0.995)
Data_Range = d.get_min_max()
Histogram_pct = [(float(index))/512 for index, value in enumerate(data) if (data[index] >= ratio[1] and data[index-1] <= ratio[1]) or (data[index] <= ratio[0] and data[index+1] >= ratio[0])]
Range = Data_Range[1]-Data_Range[0]
Color_Range = {'min': Data_Range[0]+Range*Histogram_pct[0], 'max':Data_Range[0]+Range*Histogram_pct[1]}
c.set_int32_by_name('/0/base/range-type' , 1)
c.set_double_by_name('/0/base/min', Color_Range['min'])
c.set_double_by_name('/0/base/max', Color_Range['max'])

print (Color_Range)

