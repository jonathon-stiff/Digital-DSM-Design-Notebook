#
# Import required libraries
#
from json import dumps
from IPython.display import display	
from listtablewidget import ListTableWidget

#
# List table wrapper class
#
class ListTable():
    # Initialize widget wrapper
    def __init__(self,tinput,tcaption):
	# Generate input table widget.
	self.wd = ListTableWidget(tinput=dumps(tinput),tcaption=tcaption)
	
    # Sets the list table caption after instantiation
    def set_caption(self,capval) :
	if isinstance(capval,str) : 
	    self.wd.tcaption=capval
	    self.wd.send_state()
	    
    # Sets the list table content after instantiation
    def set_input(self,tinput) :
	self.wd.tinput=dumps(tinput)
	self.wd.send_state()

    # Displays widget        
    def show(self):
        display(self.wd)
	
    # Displays widget        
    def getinstance(self):
        return self.wd