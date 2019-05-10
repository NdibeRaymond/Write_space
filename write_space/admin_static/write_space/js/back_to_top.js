$(".back-to-top").css("display","none");
jQuery(document).ready(function() {

var offset = 1000;

var duration = 300;

jQuery(window).scroll(function() {

if (jQuery(this).scrollTop() > offset) {

jQuery(".back-to-top").fadeIn(500);

} else {

jQuery(".back-to-top").fadeOut(500);

}

});



jQuery(".back-to-top").click(function(event) {

event.preventDefault();

jQuery("html, body").animate({scrollTop: 0}, duration);

return false;

})

});
