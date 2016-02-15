# Import math plotting:pyplot library
from matplotlib.pyplot import figure, close

# Import ipywidget functions
from ipywidgets import HTML, Button, VBox

# Import base64 and io library functions 
from base64 import b64encode
from io import BytesIO

#
# Class: Static figure wrapper that generates a widget output export button
#        and a HTML image widget for a generated figure 
#
class StaticFigureWrapper() :
    def __init__(self,fdpi=300,fsize=(4,3),flabel="fig") :
        # Set local variables
        self.fdpi=fdpi
        self.fsize=fsize
        self.flabel=flabel
        
        # Generate figure
        self.fig = figure(dpi=self.fdpi,figsize=self.fsize)
        close(self.fig)
        
        # Generate plot axes for the figure
        self.ax=self.fig.add_subplot(111)
        
        # Create an html widget for the figure picture
        self.outputHTML = HTML()
        
        # Create save figure widget
        self.btn = Button(description = 'Save %s' % flabel)
        self.btn.on_click(self.btnfunc)
    
    def btnfunc(self,btn): 
        self.fig.savefig('%s.png' % self.flabel , ext="png",bbox_inches='tight',dpi=self.fdpi)
    
    def plot_to_html(self):
        # write image data to a string buffer and get the PNG image bytes
        self.buf = BytesIO()
        self.fig.savefig(self.buf, format="png",bbox_inches='tight')
        self.buf.seek(0)
        return """<img src='data:image/png;base64,{}'/>""".format(b64encode(self.buf.getvalue()))
    
    def render(self) :
        self.outputHTML.value=self.plot_to_html()
        return VBox([self.outputHTML,self.btn],align="center")