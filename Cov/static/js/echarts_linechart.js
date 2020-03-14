var echarts_linechart = echarts.init(document.getElementById('left'),"vintage");

var echarts_linechart_option = {
    //标题样式
    title: {
        text: "全国累计趋势",
        textStyle: {
            color: 'black',
        },
        left: 'left',
    },
    tooltip: {
        trigger: 'axis',
        //指示器
        axisPointer: {
            type: 'line',
            lineStyle: {
                color: '#7171C6'
            }
        },
    },
    legend: {
        data: ['累计确诊', '现有疑似', '累计治愈', '累计死亡'],
        left: "right"
    },

    //图形位置
    grid: {
        left: '4%',
        right: "6%",
        bottom: '4%',
        top: 50,
        containLabel: true
    },
    xAxis: [{
        type: 'category',

        //boundaryGap: true,
        data: ['01.20', '01.21', '01.22']
    }],
    yAxis: [{
        type: 'value',
        //y轴字体设置
        axisLabel: {
            show: true,
            color: 'black',
            fontSize: 12,
            formatter: function (value) {
                if (value >= 1000){
                    value = value / 1000 + 'k';
                }
                return value;
            }
        },
        //y轴线设置显示
        axisLine: {
            show: true
        },
        //与x轴平行的线样式
        splitLine: {
            show: true,
            linStyle: {
                color: '#17273B',
                width: 1,
                type: 'solid',
            }
        }
    }],
    series: [{
        name: "累计确诊",
        type: 'line',
        smooth: true,
        data: [260, 406, 529]
    },{
       name: "现有疑似",
        type: 'line',
        smooth: true,
        data: [54, 37, 3935]
    },{
       name: "累计治愈",
        type: 'line',
        smooth: true,
        data: [25, 25, 25]
    },{
       name: "累计死亡",
        type: 'line',
        smooth: true,
        data: [6, 9, 17]
    }]
};

echarts_linechart.setOption(echarts_linechart_option)