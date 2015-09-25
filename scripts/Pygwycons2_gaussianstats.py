# Gauss filter size
size = 1.0
number_of_iteration = 21
N = 10.0
# get current datafield
d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)


#Duplicate the datafield and get its gaussian
dd_filtered = d.duplicate()
dd_filtered.filter_gaussian(N)
gwy.gwy_app_data_browser_add_data_field(dd_filter, c, 1)

#dd_filter.data_changed()
