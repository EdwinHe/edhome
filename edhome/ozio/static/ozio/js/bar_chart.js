var month="";
var cate="";
var subcate="";

var series_queue = [];
last_series = json_bar_chart_monthlyView[0];

$(function () {
	function setChart(series) {
	      chart.series[0].remove();
	      chart.addSeries(series);
	   }
	
    //$('#bar_chart_container').highcharts({
	chart = new Highcharts.Chart({
        chart: {
        	renderTo: 'bar_chart_container', 
            type: 'column'
        },
        title: {
            text: 'Monthly Expense'
        },
        subtitle: {
            text: 'Click the columns to view detail.'
        },
        xAxis: {
            type: 'category'
        },
        yAxis: {
            title: {
                text: 'Expense in AU$'
            }
        },
        legend: {
            enabled: false
        },
        exporting: {
            buttons: {
                contextButton: {
                	symbol: 'circle',
                	//symbolFill: 'blue',
                	symbolSize: 16,
                	symbolStrokeWidth: 2,
                    menuItems: null,
                    text: 'BACK',
                    onclick: function() {
                    	if (series_queue.length != 0) {
	                    	last_series = series_queue.pop();
	                    	setChart(last_series);
                    	}
                    }
                }
            }
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y:.1f}'
                },
                events: {
					click: function(event) {
						if (event.point.drilldown) { // drill down
							 this.chart.setTitle({text:event.point.drilldown});
								 
							 if (json_bar_chart_monthlyDrilldown[event.point.drilldown]) {
								 series_queue.push(last_series);
								 last_series = json_bar_chart_monthlyDrilldown[event.point.drilldown];
								 setChart(json_bar_chart_monthlyDrilldown[event.point.drilldown]);
							 } else {
								 series_queue.push(last_series);
								 last_series = json_bar_chart_monthlySubCateDrilldown[event.point.drilldown];
								 setChart(json_bar_chart_monthlySubCateDrilldown[event.point.drilldown]);
							 }
						} else {
							build_transaction_list(this.chart.title.text + ":" + event.point.name);
	                     }
					}
				}
            }
        },

        tooltip: {
            headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
            pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b> AU$<br/>'
        }, 

        /* ** Accept json_bar_chart_monthlyView as series.data **
         * series: [{
        	name: 'Monthly View, Level 1',
            colorByPoint: true,
            data: json_bar_chart_monthlyView
        }],*/
        
        // ** Accept json_bar_chart_monthlyView as series **
        series: json_bar_chart_monthlyView,
        
        //drilldown: {
        //	series: monthlyDrilldown_aslist,
        	
        	//drilldown: {
        	//	series: json_bar_chart_monthlySubCateDrilldown
        	//}
        //}
    });
});


