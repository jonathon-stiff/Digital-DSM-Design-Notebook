#
# Function: Generates automated legend and figure caption
#
def autolegcpt(fig,ctitle="Fig."):
    # Get all axes associated with the figure
    allaxes=fig.get_axes()
    ax=allaxes[0]
    lns=[];lbl=[]
    for axes in allaxes:
        lnns, lbbl = axes.get_legend_handles_labels()
        lns=lns+lnns
        lbl=lbl+lbbl

    # Add legend
    leg=ax.legend(lns,
                  lbl,
                  loc='upper center', 
                  bbox_to_anchor=(0.5, 0), 
                  ncol=2,
                  shadow=False, 
                  frameon=False)
    
    # Set legend fontsize based on x-axis font size
    labl=ax.xaxis.label
    tsize=labl.get_fontsize()
    for label in leg.get_texts():
        label.set_fontsize(tsize-1)
    
    # Set legend line width
    for label in leg.get_lines():
        label.set_linewidth(2.5)  # the legend line width
    
    # Figure caption text
    cpt=ax.text(0.5, 0,
                ctitle,
                verticalalignment='top',
                horizontalalignment='center',
                transform = ax.transAxes,
                color='black',
                fontsize=tsize
               )
    
    # Pre-draw figure in order to determine placement
    fig.canvas.draw()
    
    # Retrieve legend bounding box in axes coordinates and height
    bblg=leg.get_window_extent()
    hlg=bblg.transformed(ax.transAxes.inverted()).height
    
    # Retrieve x-axis label bounding box in axes coordinates and ymin
    bbxa=ax.xaxis.get_label().get_window_extent()
    hxa=bbxa.transformed(ax.transAxes.inverted()).ymin
    
    # Place legend and caption
    leg.set_bbox_to_anchor((0.5,hxa))
    cpt.set_position((0.5,hxa-hlg-0.1))