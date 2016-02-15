#
# Import required libraries
#
from ipywidgets.widgets import DOMWidget
from traitlets import Unicode

#
# Define list table widget    
#
class ListTableWidget(DOMWidget):
    _view_module = Unicode('nbextensions/customnb/listtable/listtablewidget', sync=True)
    _view_name = Unicode('ListTableView', sync=True)
    tinput = Unicode("", sync=True)
    tcaption = Unicode("Table I. Test.", sync=True)
	    
    # Initialize widget backend
    def __init__(self, *args, **kwargs):
        super(ListTableWidget, self).__init__(*args, **kwargs)	
