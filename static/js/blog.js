/**
 * Created by HMachine on 20/07/2016.
 */

function showMore(){
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
}

function addNewComment(){
    commentObj = $(".new-comment-textarea");
    content = commentObj.val();
    if (content) {
        //content = content.replace('\n', '<br>');
        content = content.split('\n').join('<br>');
        var d = new Date();
        var date = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
        $(".comments").prepend(
            '<div class="single-comment">' +
            '<p class="comment-meta">' + date  +
            ', by <span class="username">User</span></p>' +
            '<p>' + content + '</p>' +
            '</div>').children().first().hide().fadeIn("slow");
        //commentObj.hide();
        //$('.new-comment-submit-btn').hide();
        commentObj.val('');
        return content;
    }
}


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
        case "/newpost":
            $("a.active").removeClass("active");
            $("a.newpost-nav-item").addClass("active");
            break;
        case "/admin":
            $("a.active").removeClass("active");
            $("a.admin-nav-item").addClass("active");
            break;
    }

    //Show more characters in post
    showMore();

    if (window.location.pathname == '/'){
        var currentPage = 0;
        $(".load-more-btn").click(function(){
            currentPage++;
            $(".ajax-loader-gif").show();
            $.post('/', {'page': currentPage}, function(data){
                if(data.length == 0){
                    $(".no-more-error").show();
                    $(".load-more-btn").hide();
                }else {
                    $(".posts-wrapper").append(data);
                    showMore();
                }
            });
            $(".ajax-loader-gif").hide();
        });
    }

    //Add New Comments
    $(".write-comment-span").click(function(){
        $(this).hide();
        $(".new-comment-wrapper").slideDown('slow');
    });
    $(".new-comment-submit-btn").click(function(){
        var content = addNewComment();
        var user = $('.username').html();
        $.post(window.location.pathname, {content: content, user: user})
    });
});