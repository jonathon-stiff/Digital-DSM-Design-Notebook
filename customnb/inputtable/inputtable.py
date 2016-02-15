#
# Import required libraries
#
from ipywidgets import widgets
from traitlets import Unicode
from json import loads, dumps
from sympy.parsing.sympy_parser import parse_expr
from IPython.display import display

# Tests if a string will convert to complex
def iscomplex(x):
    try:
	fout = complex(x)
    except (ValueError, TypeError):
	return False, 0
    else:
	return True, fout
	
# Tests if a string will convert to a float
def isfloat(x):
    try:
	fout = float(x)
    except (ValueError, TypeError):
	return False, 0
    else:
	return True, fout
    
# Tests if a string is a valid sympy expression
def issympy(x):
    try:
	pout = parse_expr(x)
    except (ValueError, SyntaxError):
	return False, 0
    else:
	return True, pout
        
# Tests list index
def isindex(x,ind):
    try:
	out = x.index(ind)
    except (ValueError, SyntaxError):
	 return False, 0
    else:
	 return True, out
	    
#
# Define input table widget    
#
class InputTableWidget(widgets.DOMWidget):
    _view_module = Unicode('nbextensions/customnb/inputtable/inputtable', sync=True)
    _view_name = Unicode('InputTableWidgetView', sync=True)
    value = Unicode("", sync=True)
    tinput = Unicode("", sync=True)
    tcaption = Unicode("Table I. Test.", sync=True)
	    
    # Initialize widget backend
    def __init__(self, *args, **kwargs):
        super(InputTableWidget, self).__init__(*args, **kwargs)
        self._submission_callbacks = widgets.CallbackDispatcher()	
             
    # Loads a json string, if valid
    def ldjson(self,x):
        try:
            jsout = loads(x)
        except (ValueError, TypeError):
            return {}
        else:
            return jsout
   
    # Set jval, convert to json and set value
    def setval(self,val) :
        self.value=dumps(val)
    
    # Set jval from json converted value, return jval
    def getval(self) :
        self.jval=self.ldjson(self.value)
        return self.jval
	
#
# Input float table wrapper class
#
class InputFloatTable():
    # Initialize widget wrapper
    def __init__(self,tinput,tcaption):
        # Initialize value variable
        self.value={}
        
        # Set callbacks as empty
        self.callbacks=[]
        
        # Generate input table widget.
        self.wd = InputTableWidget(tinput=dumps(tinput),tcaption=tcaption)
        
        # Set callback function for when widget value changes
        self.wd.on_trait_change(self.valcheck, 'value')

        # Generates default values based on input list or default float
        if isinstance(tinput,list) :
            var=isindex(tinput[0],"Variable")
            val=isindex(tinput[0],"Value")
            
            if (var[0] and val[0]) :
                for k in range(1,len(tinput)) :
                    key=tinput[k][var[1]]
                    inf=isfloat(tinput[k][val[1]])
                    if inf[0] :
                        self.value[key]=inf[1]
                    else :
                        self.value[key]=2000
            else :
                self.value["none"]=0
        else :
            self.value["none"]=0
        
        # Send state
        self.wd.setval(self.value)
        self.wd.send_state()
        
    # Sets a callback function
    def setcallback(self, callback) :
        self.callbacks.append(callback)
    
    # Define callback function error checking input
    def valcheck(self,name):
        # Get widget value
        val=self.wd.getval()
        
        # Compare widget and wrapper value, update if different
        if (val!=self.value) :
            # Check each key in the widget dict value
            for key in val :
                # Preset test variables
                sout=[False,0]
                fout=[False,0]
                
                # Try sympy parser if string input value
                if isinstance(val[key],basestring) : 
                    sout=issympy(val[key])
                
                # Try convert to float if passes sym parser
                if (sout[0]) : fout=isfloat(sout[1])
                    
                # Write float value if > 1
                if (fout[0] and fout[1] > 1) :
                    # Write tested value
                    self.value[key]=fout[1]
                elif not(key in self.value and
                         isinstance(self.value[key],float) and
                         self.value[key]>1):
                    # Set default value if not existing
                    self.value[key]=float(1000)
            
            # Send value to widget
            self.wd.setval(self.value)
            self.wd.send_state()
        else :
            # Execute any defined callback functions
            for fn in self.callbacks : fn(self)

    # Displays widget        
    def show(self) :
        display(self.wd)
    
    # Get widget instance
    def getinstance(self) :
	return self.wd
	
#
# Input complex table wrapper class
#
class InputComplexTable():
    # Initialize widget wrapper
    def __init__(self,tinput,tcaption):
        # Initialize value variable
        self.value={}
	self.cvalue={}
        
        # Set callbacks as empty
        self.callbacks=[]
        
        # Generate input table widget.
        self.wd = InputTableWidget(tinput=dumps(tinput),tcaption=tcaption)
        
        # Set callback function for when widget value changes
        self.wd.on_trait_change(self.valcheck, 'value')

        # Generates default values based on input list or default float
        if isinstance(tinput,list) :
            var=isindex(tinput[0],"Variable")
            val=isindex(tinput[0],"Value")
            
            if (var[0] and val[0]) :
                for k in range(1,len(tinput)) :
                    key=tinput[k][var[1]]
                    inf=iscomplex(tinput[k][val[1]])
                    if inf[0] :
                        self.cvalue[key]=inf[1]
                    else :
                        self.cvalue[key]=0
            else :
                self.cvalue["none"]=0
        else :
            self.cvalue["none"]=0
        
	# Set value from cvalue
	for key in self.cvalue :
	    self.value[key]=str(self.cvalue[key])
	    
        # Send state
        self.wd.setval(self.value)
        self.wd.send_state()
        
    # Sets a callback function
    def setcallback(self, callback) :
        self.callbacks.append(callback)
    
    # Define callback function error checking input
    def valcheck(self,name):
        # Get widget value
        val=self.wd.getval()

        # Compare widget and wrapper value, update if different
        if (val!=self.value) :
	    # Check each key in the widget dict value
            for key in val :
		# Preset test variables
                sout=[False,0]
                fout=[False,0]
                 
                # Try sympy parser if string input value
                if isinstance(val[key],basestring) : sout=issympy(val[key])
                 
                # Try convert to float if passes sym parser
                if (sout[0]) : fout=iscomplex(sout[1])
                     
                # Write complex value if valid
                if (fout[0]) :
		    # Write tested value
                    self.cvalue[key]=fout[1]
                elif not(key in self.value and
                         isinstance(self.cvalue[key],complex)):
                    # Set default value if not existing
                    self.cvalue[key]=0
             
            # Set value from cvalue
 	    for key in self.cvalue :
		self.value[key]=str(self.cvalue[key])
 	    
 	    # Send value to widget
            self.wd.setval(self.value)
            self.wd.send_state()
        else :
	    # Execute any defined callback functions
            for fn in self.callbacks : fn(self)

    # Displays widget        
    def show(self):
        display(self.wd)
    
    # Get widget instance
    def getinstance(self) :
	return self.wd