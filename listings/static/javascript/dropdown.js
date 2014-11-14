// $( document ).ready(function() {
//     var dropNav = $("#dropdown-nav");
//  	$( "#dropdown-button" ).click(function(e) {
//  		console.log("fired");
//  		var style=dropNav.css("display");
//  		if (style=="none") {
//  			dropNav.css("display", "inline-block");
//  		} else if (style=="block"){
//  			dropNav.css("display", "none")
//  		};
//     });
 
// });

function dropdown() {
	    var dropNav = $("#dropdown-nav");
 		var style=dropNav.css("display");
 		if (style=="none") {
 			dropNav.css("display", "block");
 		} else if (style=="block"){
 			dropNav.css("display", "none")
 		};
    //form validation that recalls the page showing with supplied inputs.    
}
window.onload = function() {
    document.getElementById("dropdown-button").onclick = function() {
        dropdown();
        //validation code to see State field is mandatory.  
    }
}