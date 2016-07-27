Admin = {};
Admin.barChart = function(){
    var barCanvas = $("#barChart");
    var barChart = new Chart(barCanvas, {
        type: 'bar',
        data: {
            labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
};
Admin.pieChart = function(){
    var pieCanvas = $("#pieChart");
    var pieChart = new Chart(pieCanvas,{
        type: 'pie',
        data: {
            labels: [
                "Red",
                "Blue",
                "Yellow"
            ],
            datasets: [
                {
                    data: [300, 50, 100],
                    backgroundColor: [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56"
                    ],
                    hoverBackgroundColor: [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56"
                    ]
                }]
        },
        options: {
            animation:{
                animateScale:true
            }
        }
    });
};

Admin.managePost = function(){
        $('#manage-post-list').hideMaxListItems({
        'max':3,
        'speed':500,
        'moreText':'SHOW MORE',
        'lessText':'SHOW LESS',
        'moreHTML': '<p class="maxlist-more"><a href="#">MORE OF THEM</a></p>'
    });
};

Admin.sumTopPostNum = function(){
    var i = 0;
    var numObj = $(".top_post_number").each(function(){
        var num = parseInt($(this).html());
        $(this).html(num + i);
        i++
    });
};

Admin.changeBgClass = function(btn){
    if (btn.html() == "Enable"){
        btn.parent().parent().addClass("li-bg-red");
    }else{
        btn.parent().parent().removeClass("li-bg-red");
    }
};

Admin.liBackgroundColor = function(){
    var adminBtn = $(".disable-admin-btn");
    adminBtn.each(function(){
        Admin.changeBgClass($(this));
    });
};

Admin.enableDisablePost = function(){
    $('.disable-admin-btn').click(function(){
        var postId = parseInt($(this).siblings().filter('input.enable-disable-post-id').val());
        var status = true;
        if ($(this).html() == "Enable"){
            status = false;
        }
        $.post('/admin',{post_id: postId, status: status});
        if (status){
            $(this).html('Enable');
        }else{
            $(this).html('Disable');
        }
        Admin.changeBgClass($(this));
    });

    //$.post('/admin',{post_id: postId, status: status});

};

Admin.init = function(){
    Admin.barChart();
    Admin.pieChart();
    Admin.managePost();
    Admin.sumTopPostNum();
    Admin.liBackgroundColor();
    Admin.enableDisablePost();
    //$('.disable-admin-btn').click(Admin.enableDisablePost($(this)));

};

$(document).ready(function(){
    Admin.init();

});
