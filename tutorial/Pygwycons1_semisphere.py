# semisphere radius
radius = 100.0
# position in datafield resolution
x0 = 100
y0 = 100
z0 = -30
# scaling factor
factor = 10e-12

# get active datafield
d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
# create new datafield by using active datafield and
# set its values to zero
sphere_datafield = d.new_alike(True)
for y in range(d.get_yres()):
  for x in range(d.get_xres()):
    z = pow(radius, 2) - pow(x - x0, 2) - pow(y - y0, 2)
    if (z > 0):
      # set datafield's value
      sphere_datafield.set_val(x, y, (z-z0)*factor)

# get active container
c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
# add sphere datafield to active container
gwy.gwy_app_data_browser_add_data_field(sphere_datafield, c, 3)