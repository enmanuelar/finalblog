/**
 * Created by HMachine on 20/07/2016.
 */
$(document).ready(function(){
    switch (window.location.pathname){
        case "/":
            $("a.active").removeClass("active");
            $("a.home-nav-item").addClass("active");
            break;
        case "/signup":
            $("a.active").removeClass("active");
            $("a.signup-nav-item").addClass("active");
            break;
        case "/login":
            $("a.active").removeClass("active");
            $("a.login-nav-item").addClass("active");
            break;
        case "/admin":
            $("a.active").removeClass("active");
            $("a.admin-nav-item").addClass("active");
            break;
    }

    //Show more/ less blog post body
    // Configure/customize these variables.
    var showChar = 330;  // How many characters are shown by default
    var ellipsestext = "...";
    var moretext = "Show more >";
    var lesstext = "Show less";


    $('.more').each(function() {
        var content = $(this).html();

        if(content.length > showChar) {

            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);

            var html = c + '<span class="moreellipses">' + ellipsestext+ '&nbsp;</span><span class="morecontent"><span>' + h +
                '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';

            $(this).html(html);
        }

    });

    $(".morelink").click(function(){
        if($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });
});