$( "#transaction_breakdown_dialog" ).dialog({
	autoOpen: false,
	title: 'Transaction Breakdown',
	dialogClass: 'ed-dialog-flatly',
	width: '90%',
	hight: 'auto',
	maxHeight: 600,
	modal: true,
	show: {
		duration: 300
	},
});

function build_transaction_list(date_cate_subcate) {
	yyyymm = date_cate_subcate.split(':')[0];
	cate = date_cate_subcate.split(':')[1];
	subcate = date_cate_subcate.split(':')[2];
	
	cate = cate.replace('&','%26');
	subcate = subcate.replace('&','%26');
	url = '/API/transaction/?yyyymm=' + yyyymm + '&cate=' + cate + '&subcate=' + subcate
	
	$.ajax(
			{	type: "GET", 
				async: false, 
				url: url, 
				success: function(objs) {
					$('#transaction_breakdown_dialog').empty();
					
					var content = "";
					content += '<div>';
					content += '<table class="table table-striped table-hover">';
					content += '<thead>';
					content += '<tr class="success">';
					
					//Build Column Name
					for (var col in objs[0]) {
						content += '<th>' + col + '</th>';
					}
					
					content += '</tr>';
					content += '</thead>';
					content += '<tbody>';
					
					for (var i = 0; i < objs.length; i++) {
						content += '<tr>';
						for (var c in objs[i]) {
							content += '<td>' + objs[i][c] + '</td>';
						}
						content += '</tr>';
					}
					content += '</tbody>';
					content += '</table>';
					content += '</div>';
					
					$('#transaction_breakdown_dialog').append(content);
				}
			}
		);
	
	$("#transaction_breakdown_dialog").dialog( "open" );
}