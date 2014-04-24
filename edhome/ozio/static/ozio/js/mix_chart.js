$(function () {
    $('#mix_chart_container').highcharts({
    	chart: {
            zoomType: 'x'
        },
        title: {
            text: 'Income/Expense and Balance'
        },
        plotOptions: {
            series: {
                pointInterval: 24 * 3600 * 1000 * 30.436,
                pointStart: Date.UTC(2013, 10, 01),
            }
        },
        xAxis: {
            //categories: ['Apples', 'Oranges', 'Pears', 'Bananas', 'Plums']
        	type: 'datetime',
        	minRange: 24 * 3600 * 1000 * 30.436 // 1 month
        },
    	yAxis: [{ // Primary yAxis
            labels: {
                //format: '{value} AU$',
            	style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            title: {
                text: 'I/O in AU$',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true

        }, { // Secondary yAxis
            gridLineWidth: 0,
            title: {
                text: 'Balance in AU$',
                style: {
                    color: Highcharts.getOptions().colors[2]
                }
            },
            labels: {
                //format: '{value} AU$',
                style: {
                    color: Highcharts.getOptions().colors[2]
                }
            }
        }],
        series: json_mix_chart_data
        /*
        series: [{
            type: 'column',
            name: 'Jane',
            data: [3, 2, 1, 3, 4]
        }, {
            type: 'column',
            name: 'John',
            data: [2, 3, 5, 7, 6]
        }, {
            type: 'spline',
            name: 'Average',
            data: [3, 2.67, 3, 6.33, 3.33],
            marker: {
            	lineWidth: 2,
            	lineColor: Highcharts.getOptions().colors[3],
            	fillColor: 'white'
            }
        }]
        */
    });
});
    
