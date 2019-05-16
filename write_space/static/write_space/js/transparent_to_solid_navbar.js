$(window).on('load', function(){
  if($(window).width()<=786){
    $("#big_nav").addClass("hidden");
    $("#small_nav").removeClass("hidden");
  }else{
    $("#big_nav").removeClass("hidden");
    $("#small_nav").addClass("hidden");

  }
  if($(window).width()<=1000){
    $("#Poll1_1").addClass("hidden");
    $("#Poll1_2").addClass("hidden");
    $("#Poll1_3").addClass("hidden");
  }else{
    $("#Poll1_1").removeClass("hidden");
    $("#Poll1_2").removeClass("hidden");
    $("#Poll1_3").removeClass("hidden");

  }
  if($(window).width()<=700){
    $("#Poll2_1").addClass("hidden");
    $("#Poll2_2").addClass("hidden");

  }else{
    $("#Poll2_1").removeClass("hidden");
    $("#Poll2_2").removeClass("hidden");


  }
  if($(window).width()<=500){
    $("#Poll3_1").addClass("hidden");
    $("#Poll3_2").addClass("hidden");

  }else{
    $("#Poll3_1").removeClass("hidden");
    $("#Poll3_2").removeClass("hidden");


  }


    })

$(window).on("resize", function(){
  if($(window).width()<=786){
    $("#big_nav").addClass("hidden");
    $("#small_nav").removeClass("hidden");
  }else{
    $("#big_nav").removeClass("hidden");
    $("#small_nav").addClass("hidden");

  }
  if($(window).width()<=1000){
    $("#Poll1_1").addClass("hidden");
    $("#Poll1_2").addClass("hidden");
    $("#Poll1_3").addClass("hidden");
  }else{
    $("#Poll1_1").removeClass("hidden");
    $("#Poll1_2").removeClass("hidden");
    $("#Poll1_3").removeClass("hidden");

  }
  if($(window).width()<=700){
    $("#Poll2_1").addClass("hidden");
    $("#Poll2_2").addClass("hidden");

  }else{
    $("#Poll2_1").removeClass("hidden");
    $("#Poll2_2").removeClass("hidden");


  }
  if($(window).width()<=500){
    $("#Poll3_1").addClass("hidden");
    $("#Poll3_2").addClass("hidden");

  }else{
    $("#Poll3_1").removeClass("hidden");
    $("#Poll3_2").removeClass("hidden");


  }


    })


//

/**
 * Listen to scroll to change header opacity class
 */
function checkScroll(){

    var startY = $('.navbar.top_nav').height() * 0.1; //The point where the navbar changes in px

    if($(window).scrollTop() > startY){
        $('.navbar.top_nav').addClass("scrolled");
    }else{
        if(($("#bs-example-navbar-collapse-1").is(":visible")) == false){
        console.log("toggle is open")};
        $('.navbar.top_nav').removeClass("scrolled");
    }
}

if($('.navbar.top_nav').length > 0){
    $(window).on("scroll load resize", function(){
        checkScroll();
    });
}


$(".navbar-toggle.collapsed").on("click", function(){
  if(($("#bs-example-navbar-collapse-1").is(":visible")) == false){
  console.log("toggle is open");
  $('.navbar.top_nav').addClass("scrolled");}else{
    checkScroll();
  };})


/******************************************************************************/
      /********************privacy policy listener script***************/

      $("#privacy_policy").on("click",function(){

        $(".privacy_policy").removeClass("hidden");
        $("#privacy_policy").addClass("current");


        $(".terms_of_use").addClass("hidden");
        $("#terms_of_use").removeClass("current");
      })



      $("#terms_of_use").on("click",function(){

        $(".terms_of_use").removeClass("hidden");
        $("#terms_of_use").addClass("current");


        $(".privacy_policy").addClass("hidden");
        $("#privacy_policy").removeClass("current");
      })
      /********************privacy policy listener script***************/
/******************************************************************************/


// 786




   //  var elmnt = document.createElement("li");
   //     var textnode = document.createTextNode("Water");
   //     elmnt.appendChild(textnode);
   //
   //     var item = document.getElementById("myList");
   //     item.replaceChild(elmnt, item.childNodes[0]);
   // }

    // var textnode = document.createTextNode("Water");
    //     var item = document.getElementById("myList").childNodes[0];
    //     item.replaceChild(textnode, item.childNodes[0]);
    // }
