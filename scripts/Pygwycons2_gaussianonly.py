# Gauss filter size
size = 1.0
number_of_iteration = 21
N = 10.0
# get current datafield
c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)


dd_filtered = d.duplicate()
dd_filtered.filter_gaussian(10.0)
#gwy.gwy_app_data_browser_add_data_field(dd_filtered, c, TRUE)
#(Put datafield , into the container , by showing the data on screen)
gwy.gwy_app_data_browser_add_data_field(dd_filtered, c, 1)

#dd_filter.data_changed()
