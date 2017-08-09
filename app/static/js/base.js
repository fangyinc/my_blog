$(document).ready(function() {

    if($(window).width() < 995) {
            $("#right-index").hide();
            $("div#post-index").removeClass("col s9");
            $("div#right-index").removeClass("col s3");
        }
        else{
            $("#right-index").show();
            $("div#post-index").addClass("col s9");
            $("div#right-index").addClass("col s3");
    }
    $(window).resize(function() {   //根据屏幕大小调整侧边栏
        if($(window).width() < 995) {
            $("#right-index").hide();
            $("div#post-index").removeClass("col s9");
            $("div#right-index").removeClass("col s3");
        }
        else{
            $("#right-index").show();
            $("div#post-index").addClass("col s9");
            $("div#right-index").addClass("col s3");
        }
    });

  $('.button-collapse').sideNav({
      menuWidth: 300, // Default is 300
      edge: 'left', // Choose the horizontal origin
      closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
      draggable: true, // Choose whether you can drag to open on touch screens,
      onOpen: function(el) { /* Do Stuff*/ }, // A function to be called when sideNav is opened
      onClose: function(el) { /* Do Stuff*/ }// A function to be called when sideNav is closed
    }
  );

  $('.collapsible').collapsible();
    //跳到顶部
    $('div#base_container').prepend('<a href="#" class="my-back-to-top">Back to Top</a>');
    var amountScrolled = 300;
    $(window).scroll(function () {
        if ($(window).scrollTop() > amountScrolled) {
            $('a.my-back-to-top').fadeIn('slow');
        } else {
            $('a.my-back-to-top').fadeOut('slow');
        }
    });
    $('a.my-back-to-top').click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 700);
        return false;
    });

    //显示友链
    $('.modal').modal({
            dismissible: true, // Modal can be dismissed by clicking outside of the modal
            opacity: .5, // Opacity of modal background
            inDuration: 300, // Transition in duration
            outDuration: 200, // Transition out duration
            startingTop: '4%', // Starting top style attribute
            endingTop: '10%', // Ending top style attribute
            ready: function (modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
                //alert("Ready");
                console.log(modal, trigger);
            },
            complete: function () {
            }//alert('Closed')} // Callback for Modal close
        }
    );

});