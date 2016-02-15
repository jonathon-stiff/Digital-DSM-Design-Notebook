# Import math plotting patches library
from matplotlib.patches import Circle

# Import numerical function library
from numpy import unique, concatenate, amax

#
# Checks list and converts to complex list, if possible
#
def complexlist(clist) :
    if type(clist)==list :
        try :
            out=[complex(cl) for cl in clist]
        except (ValueError,SyntaxError,NameError) :
            return []
        else :
            return out
    else :
        return []

#
# Plots z-plane pole-zero plot 
#
def zplane(ax, z, p, ctitle="",
           pcolor='red',zcolor='blue',
           mkrsize=10,mkredge=3,fsize=12
          ):
    # Set common variables
    ccolor='gray'
    
    # Find the plot figure from axes
    fig=ax.get_figure()
    
    # Check pole-zero list, convert to proper format
    zlist=complexlist(z)
    plist=complexlist(p)

    # Determine unique poles,zeros and number of each
    upoles, upcnt = unique(plist, return_counts=True)
    uzeros, uzcnt = unique(zlist, return_counts=True)
    
    # Add unit circle    
    unit_circle = Circle((0,0), radius=1,
                         fill=False, color=ccolor,
                         ls='solid'
                        )
    ax.add_patch(unit_circle)
    
    # Plot the poles and set marker properties
    ax.plot(upoles.real, upoles.imag, 'x',
            markersize=mkrsize,
            markeredgewidth=mkredge,
            markeredgecolor=pcolor,
            markerfacecolor='none',
            label="poles"
           )
    
    # Plot the zeros and set marker properties
    ax.plot(uzeros.real, uzeros.imag,  'o', 
            markersize=mkrsize, 
            markeredgewidth=mkredge,
            markeredgecolor=zcolor,
            markerfacecolor='none',
            label="zeros"
           )
    
    # Label multi-pole markers
    for k in range(len(upoles)):
        if upcnt[k]>1 : ax.annotate('%d' % upcnt[k], 
                                    (upoles[k].real,upoles[k].imag),
                                    xycoords='data',
                                    xytext=(5, 5), 
                                    textcoords='offset points',
                                    size=fsize,
                                    color=pcolor
                                   )
    for k in range(len(uzeros)):
        if uzcnt[k]>1 : ax.annotate('%d' % uzcnt[k], 
                                    (uzeros[k].real,uzeros[k].imag),
                                    xycoords='data',
                                    xytext=(5, 5), 
                                    textcoords='offset points',
                                    size=fsize,
                                    color='blue'
                                   )

    # Symmetrically scale axes to fit
    r = 1.1 * amax(concatenate((abs(uzeros), abs(upoles), [1])))
    ax.axis('scaled')
    ax.axis([-r, r, -r, r])

    # Set spines for zero intercept axes and ticks
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_smart_bounds(True)
    ax.spines['bottom'].set_smart_bounds(True)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    # Setup axis labels
    ax.set_xlabel('Re', fontsize = fsize)
    ax.xaxis.set_label_coords(1.05, 0.51,transform=None)
    yl=ax.set_ylabel('Im', fontsize = fsize)
    yl.set_rotation('horizontal')
    ax.yaxis.set_label_coords(0.5, 1.01,transform=None)
    
    # Remove y-axis 0 tick label
    xlst = ax.get_xticks().tolist()
    ylst = ax.get_yticks().tolist()
    ax.xaxis.get_majorticklabels()[xlst.index(0)].set_horizontalalignment("left")
    xlst[xlst.index(0)]='0'
    ylst[ylst.index(0)]=''
    ax.set_xticklabels(xlst)
    ax.set_yticklabels(ylst)
    
    # Get all axes associated with the figure
    lns, lbl = ax.get_legend_handles_labels()

    # Add legend
    leg=ax.legend(lns,lbl,
                  loc='upper center', 
                  bbox_to_anchor=(0.5, 0), 
                  ncol=2,
                  shadow=False, 
                  frameon=False,
                  numpoints = 1
                 )
    
    # Set legend fontsize based on x-axis font size
    for label in leg.get_texts() : label.set_fontsize(fsize-1)
    
    # Figure caption text
    cpt=ax.text(0.5, 0, ctitle, color='black', 
                fontsize=fsize,
                verticalalignment='top',
                horizontalalignment='center',
                transform = ax.transAxes
               )
    
    # Pre-draw figure in order to determine placement
    fig.canvas.draw()
    
    # Retrieve legend bounding box in axes coordinates and height
    lgbb=leg.get_window_extent()
    lgh=lgbb.transformed(ax.transAxes.inverted()).height
    
    # Place caption below legend
    cpt.set_position((0.5,-lgh-0.1))