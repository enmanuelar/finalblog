Blog = {};
Blog.showMore = function() {
    //Show more/ less blog post body
    // Configure/customize these variables.
    var showChar = 330;  // How many characters are shown by default
    var ellipsestext = "...";
    var moretext = "Show more >";
    var lesstext = "Show less";


    $('.more').each(function () {
        var content = $(this).html();

        if (content.length > showChar) {

            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);

            var html = c + '<span class="moreellipses">' + ellipsestext + '&nbsp;</span><span class="morecontent"><span>' + h +
                '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';

            $(this).html(html);
        }

    });

    $(".morelink").click(function () {
        if ($(this).hasClass("less")) {
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
};

Blog.addNewComment = function() {
    var commentObj = $(".new-comment-textarea");
    var content = commentObj.val();
    if (content) {
        var username = $("#hidden-comment-username").val();
        content = content.split('\n').join('<br>');
        var d = new Date();
        var date = d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
        $(".comments").prepend(
            '<div class="single-comment">' +
            '<p class="comment-meta">' + date +
            ', by <span class="username">' + username + '</span></p>' +
            '<p>' + content + '</p>' +
            '</div>').children().first().hide().fadeIn("slow");
        commentObj.val('');
        return content;
    }
};

Blog.changeValidTagClass = function changeValidTagClass(targetTag, status) {
    if (status) {
        $(targetTag).removeClass("has-success has-error").addClass("has-success").children("span.glyphicon").removeClass("glyphicon-ok glyphicon-remove").addClass("glyphicon-ok");
    } else{
        $(targetTag).removeClass("has-success has-error").addClass("has-error").children("span.glyphicon").removeClass("glyphicon-ok glyphicon-remove").addClass("glyphicon-remove");
    }
};

Blog.titleValidation = function(element){
    $(element).blur(function() {
        $.post('/validation',{title: element.val()}, function(data){
            console.log('yee');
            var isValid = JSON.parse(data);
            if (!isValid.valid_title){
                $(".newpost-submit-btn").prop("disabled", true);
            }else {
                $(".newpost-submit-btn").prop("disabled", false);
            }
            Blog.changeValidTagClass(element.parent(), isValid.valid_title);
        });
    });
};

Blog.signupValidation = function(){
    //username
    $("#input-name").blur(function () {
        var username = $("#input-name").val();
        var validation = $("input#validation-input").val();
        if (username && /^[a-zA-Z0-9_-]{3,20}$/.test(username)) {
            $.post("/signup", {username: username, validation: validation}).done(function(data){
                var status = JSON.parse(data).status;
                Blog.changeValidTagClass("#input-name-div", status);
            });
        }
        else {
            Blog.changeValidTagClass("#input-name-div", false);
        }
    });
//password
    $("#input-password").change(function () {
        var password = $("#input-password").val();
        var verify = $("#input-verify").val();

        if (password && /^.{3,20}$/.test(password)) {
            Blog.changeValidTagClass("#input-password-div", true);
            if (verify && verify == password){
                Blog.changeValidTagClass("#input-verify-div", true);
            }
        }
        else {
            Blog.changeValidTagClass("#input-password-div", false);
        }
    });
//verify
    $("#input-verify").change(function () {
        var verify = $("#input-verify").val();
        var password = $("#input-password").val();
        if (verify && /^.{3,20}$/.test(verify) && (password == verify)) {
            Blog.changeValidTagClass("#input-verify-div", true);
        }
        else {
            Blog.changeValidTagClass("#input-verify-div", false);
        }
    });
//email
    var email = $("#input-email");
    if (email.val()){
        email.blur(function () {
            var email = $("#input-email").val();
            if ((email && /^[\S]+@[\S]+.[\S]+$/.test(email)) || !email) {
                Blog.changeValidTagClass("#input-email-div", true);
            }
            else {
                Blog.changeValidTagClass("#input-email-div", false);
            }
        });
    }
    //Signup submit btn
    $("#register-btn").click(function(){
        if ($("div.has-feedback").children("span.glyphicon-ok").length >= 3){
            $("input#validation-input").val("false");
        }else{
            $("#input-password").val("");
            $("#input-password-div").removeClass("has-success has-error").children("span.glyphicon").removeClass("glyphicon-ok glyphicon-remove");
            $("#input-verify").val("");
            $("#input-verify-div").removeClass("has-success has-error").children("span.glyphicon").removeClass("glyphicon-ok glyphicon-remove");

        }
    });
};

Blog.editPost = function(){
    $('.edit-save-btn').click(function(){
        var content = $('.contenteditable').html();
        var post_id = window.location.href.slice(window.location.href.indexOf('?') + 9);
        $.post('/edit',{post_id: post_id, content: content});
    });
};

Blog.init = function(){
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
    Blog.showMore();

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
                    Blog.showMore();
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
        var content = Blog.addNewComment();
        var user = $('.username').html();
        var category = $('i.category').html().substring(1);
        $.post(window.location.pathname, {content: content, user: user, category: category})
    });

    //New post title validation
    Blog.titleValidation($("#newpost-title"));

    //Signup Validation
    Blog.signupValidation();

    //Edit Post
    Blog.editPost();
};
$(document).ready(function(){
    Blog.init();
});







