//var province_data = JSON.parse(window.localStorage.getItem('province_name'))

function gettime(){
    $.ajax({
        url:"/time",
        timeout:10000,//超时时间设置为10秒
        success:function(data){
            $("#time").html(data)
        },
        error:function(xhr,type,errorThrown){

        }
    });
}

function get_centerA_data(){
    $.ajax({
        url:"/centerA",
        success:function(data) {
            $(".num h1").eq(0).text(data.confirm);
            $(".num h1").eq(1).text(data.suspect);
            $(".num h1").eq(2).text(data.heal);
            $(".num h1").eq(3).text(data.dead);
            },
        error:function(xhr,type,errorThrown){

        }
    })
}


function get_centerB_data(){
    $.ajax({
        url:"/centerB",
        success: function(data)
        {
            echarts_map_option.series[0].data = data.data
            echarts_map.setOption(echarts_map_option)
        },
        error:function(xhr,type,errorThrown){

        }
    })
}

/*function get_detail(){
    $.ajax({
        url:"/detail",
        success:function(data)
        {
             $("#province").text(province_data);
            //document.getElementById("province").innerHTML = localStorage.getItem("province_name");
        },
        error:function(){

        }
    })
}*/

gettime()
get_centerA_data()
get_centerB_data()
//get_detail()
//setInterval(gettime,1000)
//setInterval(get_centerA_data,1000)