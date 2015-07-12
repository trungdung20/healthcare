$('span.stars').stars();
$.fn.stars = function(){
	return $(this).each(function(){ 
	//get the value 
	var val = parseFloat($(this).html());
	//Make sure that the value is in 0-5 range, multiply to get width
	
	var size = Math.max(0,(Math.min(5,val))) * 16;
	//Create stars holder
	var $span = $('<span/>').width(size);
	//Replace the numberical value with stars
	$(this).html($span);
	});
}