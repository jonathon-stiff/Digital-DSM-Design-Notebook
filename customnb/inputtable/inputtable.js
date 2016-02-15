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
    var InputTableWidgetView = widget.DOMWidgetView.extend({
        render: function(){
            var i, k,tstring,tdata,varx,valx;
            var that=this;
            var tjson=this.model.get('tinput');
	    
	    // Insert table css values
            this.$tcss=$("<link />")
	        .attr("rel","stylesheet")
		.attr("type","text/css")
		.attr("href","../nbextensions/inputtable/inputtable.css")
	        .appendTo(this.$el);
            
            // Insert table declaration
            this.$el.append($("<table class='lt'>"));
            
            // Insert table caption
            this.$label = $("<caption class='clt' />")
                .appendTo(this.$el)
                .hide();
            
            // Set empty list of input references
            this.$inputs=[];
            
            // Write table string if tdata is valid json
            if (isJSON(tjson)) {
                tdata = $.parseJSON(this.model.get('tinput'));
                
                // Generate the table header html string from the json data keys
                this.$el.append($("<tr>"));
                for(k=0; k<tdata[0].length; k++) {
                   $("<th class='ltable' />").html(tdata[0][k]).appendTo(this.$el);
                }
                this.$el.append($("</tr>"));
   
                // Find variable and value columns
                varx=tdata[0].indexOf("Variable");
		valx=tdata[0].indexOf("Value");
		
		// Generate the rest of the string html table rows
		for(i=1; i<tdata.length; i++) {
		    this.$el.append($("<tr>"));
		    for(k=0; k<tdata[i].length; k++) {
			if (k==valx) {			    
			    this.$inputs[i-1]=$("<input type='text' size=12 />")
			        .attr("id",tdata[i][varx]);
			    $("<td class='ltable' />").html(this.$inputs[i-1]).appendTo(this.$el);
			} else {
			    $("<td class='ltable' />").html(tdata[i][k]).appendTo(this.$el);
			}
		    }
		    this.$el.append($("</tr>"));
                }
            }
            // End table declaration
            this.$el.append($("</table>"));
            
            // Listen for changes specifically to tcaption
            this.listenTo(this.model, 'change:tcaption', 
                          function(sender, value) {
                             that.updateCaption();
                          }, this);
            
            // Handle table change
            this.updateCaption();
            this.update();
        },
        updateCaption: function() {
            // Get model caption
            var caption = this.model.get('tcaption');

            // Hide caption if empty/undefined, otherwise show
            if (caption === undefined || caption.length === 0) {
                this.$label.hide();
            } else {
                this.typeset(this.$label, caption);
                this.$label.show();
            }
        },
        update: function(options) {
            // Python --> Javascript update.
            var i, $inp, fix=false, 
                json, newdata={}, data={};
            
            // Get input values from model.
            var djson = this.model.get('value');
            
            // Write json to data if valid 
            if (isJSON(djson)) data=$.parseJSON(djson);
            
            // Check data matches input ids, write valid values
            for (i=0; i<this.$inputs.length; i++) {
                $inp=this.$inputs[i];
                if (data[$inp.attr("id")]!=undefined &&
                    data[$inp.attr("id")]!=""
                ){
                    $inp.val(data[$inp.attr("id")]);
                    newdata[$inp.attr("id")]=data[$inp.attr("id")];
                }
                else {
                    newdata[$inp.attr("id")]="1000";
                    $inp.val(newdata[$inp.attr("id")]);
                    fix=true;
                }

            }
            // Update the widget value if changes occured
            if (fix) {
                // Get the data, and serialize it in JSON.
                json = JSON.stringify(newdata);
                
                // Update the model with the JSON string.
                this.model.set('value', json);
                this.touch();
            }
            return InputTableWidgetView.__super__.update.apply(this);
        },
 
        // Tell Backbone to listen to the change event of input controls.
        events: {
           "change"         : "handle_table_change",
           "keypress input" : "handleKeypress"
        },
        
        // Trigger unfocus input when enter key pressed, trigger change
        handleKeypress: function(e) { 
            if (e.keyCode == 13) {
               // unfocus input
               // Stop event propagation
               $('*:focus').blur();
               e.stopPropagation();
               e.preventDefault();
               return false;
            }
        },    
        // Handles changes in the table from an input change                                            
        handle_table_change: function(event) {
           // Javascript --> Python update.

           // Get input values from model.
           var json, data;
           var djson = this.model.get('value');
            
           // Write json to data if valid 
           if (isJSON(djson)) data=$.parseJSON(djson);
           
           // Obtain the input pointer, id and value
	   var $inp=$(event.target);
           var id=$inp.attr('id');
           var val=$inp.val();
            
           // Capture input value if data id exists and 
           // value is a number, otherwise write previous value.
           if (data[id]!=undefined) {
	       // Write input value to data
               data[id]=val;
                  
               // Get the data, and serialize it in JSON.
               json = JSON.stringify(data);
                   
               // Update the model with the JSON string.
               this.model.set('value', json);
               this.touch();
           }
           else {
               this.update();
           }
        }
    });
    return {
        InputTableWidgetView, InputTableWidgetView
    }
}); 