Admin = {};
Admin.barChart = function(){
    var barCanvas = $("#barChart");
    var barChart = new Chart(barCanvas, {
        type: 'bar',
        data: {
            labels: ["Random", "Music", "Science", "Technology", "Funny"],
            datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
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
Admin.pieChart = function(data){
    var pieCanvas = $("#pieChart");
    console.log(data.data);
    $('.top-categories-row').each(function(){
        $(this).children('')
    });
    var pieChart = new Chart(pieCanvas,{
        type: 'pie',
        data: {
            labels: ["Random", "Music", "Science", "Technology", "Funny"],
            datasets: [
                {
                    data: data.data,
                    backgroundColor: [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56",
                        "#96FF56",
                        "#F556FF"
                    ],
                    hoverBackgroundColor: [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56",
                        "#96FF56",
                        "#F556FF"
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

Admin.sumTopPostNum = function(obj){
    var i = 0;
    obj.each(function(){
        var num = parseInt($(this).html());
        $(this).html(num + i);
        i++
    });
};

Admin.changeBgClass = function(btn){
    if (btn.html() == "Enable"){
        btn.parent().parent().parent().addClass("li-bg-red");
    }else{
        btn.parent().parent().parent().removeClass("li-bg-red");
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
};

Admin.get_charts_data = function(){
    $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/charts'
    }).done(function(data){
        Admin.pieChart(data);
    });
};

Admin.init = function(){
    Admin.managePost();
    Admin.sumTopPostNum($(".top_post_number"));
    Admin.sumTopPostNum($(".top_categories_number"));
    Admin.liBackgroundColor();
    Admin.enableDisablePost();
    Admin.barChart();
    Admin.get_charts_data();
};

$(document).ready(function(){
    Admin.init();

});
