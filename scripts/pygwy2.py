# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 20:58:12 2015

@author: June
"""

# This is required for usage of pygwy functions

import gwy

plugin_menu = "/Correct Data/Invertss"
plugin_type = "PROCESS"

def run():
    #Create undo poin, the detailed explanation of the step is
    #beyond this tutorial, Basically the active container and datatield key are used for storing information to undo stack
    key = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_KEY)
    gwy.gwy_app_undo_qcheckpointv(gwy.data, key)
    
    # Get active datafield and store it to 'd' variable. The variable is object of type gwy.DataField
    d = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
    
    # Call invert function(do not invert x and y axes, invert only z axis)
    d.invert(0, 0, 1)
    
    # Report data change to Gwyddion, this is required to update(redraw) graphical presentation of datafield in application window
    d.data_changed()
    
