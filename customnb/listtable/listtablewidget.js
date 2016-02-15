//
// Check if data is json format
//
function isJSON(msg) {
   // Get the model's JSON string, and parse it.
   var IS_JSON = true;
    
   // Try parsing msg, set IS_JSON false if an error is generated
   try {
       var json = $.parseJSON(msg); 
   } catch(err) {
       IS_JSON = false;
   } 
   // Returns true if valid json parse and > 0 data length
   return (IS_JSON && json.length!=0);
}

//
// Defines an html input table
//
define(["jquery",
        "nbextensions/widgets/widgets/js/widget"
], function($, widget) {
    var ListTableView = widget.DOMWidgetView.extend({
        render: function(){
            var i, k,tstring,tdata,varx,valx;
	    var that=this;

	    
	    // Insert table css values
            this.$tcss=$("<link />")
	        .attr("rel","stylesheet")
		.attr("type","text/css")
		.attr("href","../nbextensions/customnb/listtable/listtablewidget.css")
	        .appendTo(this.$el);
            
            // Insert div
            this.$el.append($("<div class='lt' />"));
	    
	    // Insert table declaration
            this.$el.append($("<table class='lt'>"));
            
            // Insert table caption
            this.$label=$("<caption class='clt' />")
                .appendTo(this.$el)
                .hide();
		
	    // Insert table content
	    this.$content=$('<tr><td>There are no items...</td></tr>')
	        .appendTo(this.$el);
		
	    // End table declaration
            this.$el.append($("</table>"));
		
            // Handle table caption update
            this.updateCaption();
	    
	    // Handle table content update
            this.updateContent();
	    
            // Listen for changes specifically to tcaption
            this.listenTo(this.model, 'change:tcaption', 
                          function(sender, value) {
                             that.updateCaption();
                          }, this);
	    
	    // Listen for changes specifically to tcaption
            this.listenTo(this.model, 'change:tinput', 
                          function(sender, value) {
                             that.updateContent();
                          }, this);

	    // Look for and render any mathjax expressions in the html
	    MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
        },
        updateCaption: function() {
            // Get model caption value
            var caption = this.model.get('tcaption');

            // Hide caption if empty/undefined, otherwise show
            if (caption === undefined || caption.length === 0) {
                this.$label.hide();
            } else {
                this.typeset(this.$label, caption);
                this.$label.show();

            }
        },
	updateContent: function() {
	    var tjson=this.model.get('tinput');
	    var tcontent="", tdata, k, i;
			
	    // Write table string if tdata is valid json
            if (isJSON(tjson)) {
                tdata = $.parseJSON(this.model.get('tinput'));
		
		// Generate the rest of the string html table rows
		for(i=0; i<tdata.length; i++) {
		    tcontent+="<tr>";
		    for(k=0; k<tdata[i].length; k++) {
			if (i==0) {			    
			    tcontent+="<th class='ltable'>"+tdata[i][k]+"</th>";
			} else {
			    tcontent+="<td class='ltable'>"+tdata[i][k]+"</td>";
			}
		    }
		    tcontent+="</tr>";
                }
            }
	    // Write new table content
	    this.$content.html(tcontent);   
        }
    });
    return {
        ListTableView, ListTableView
    }
}); 