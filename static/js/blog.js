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
        case "/admin":
            $("a.active").removeClass("active");
            $("a.admin-nav-item").addClass("active");
            break;
    }
});