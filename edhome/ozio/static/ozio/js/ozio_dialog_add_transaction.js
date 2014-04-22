$( "#new_transaction_dialog" ).dialog({
	autoOpen: false,
	title: 'ADD NEW TRANSACTION (MANUAL)',
	dialogClass: 'ed-dialog-flatly',
	width: 'auto',
	height: 'auto',
	modal: true,
	show: {
		duration: 300
	},
	beforeClose: function() {$("#add_transaction_message").css("display", "none");},
});

var new_keyword_option_text = '(Use New Keyword)';

$( "#add_new_transaction" ).click(function() {
	
	// Build keyword drop down
	url = '/API/keyword/?keyword_like=general';
	$.ajax(
			{	type: "GET", 
				async: false, 
				url: url, 
				success: function(objs) {
					$('#id_info-keyword').empty();
					var content = "";
					content += '<option value="" selected="selected">' + new_keyword_option_text + '</option>';
					
					for (var i = 0; i < objs.length; i++) {
						content += '<option value=' + toString(i) + '>' + objs[i]['keyword'] + '</option>'
					}
					$('#id_info-keyword').append(content);
				}
			}
	);
	
	$( "#new_transaction_dialog" ).dialog( "open" );
});

function on_AddTran_Click_Cancel(){
	$("#new_transaction_dialog").dialog("close");
	return false;
}

function on_AddTran_Click_Add(){
	
	// Collect and Build Transaction Fields
	date = $('#id_transaction-date').val();
	amount = $('#id_transaction-amount').val();
	
	if ($('#id_info-keyword :selected').text() == new_keyword_option_text)
		info = $('#id_transaction-info').val();
	else
		info = $('#id_info-keyword :selected').text() + ': ' + $('#id_transaction-info').val();
	
	original_info = info;
	source_file = $('#id_transaction-source_file').val();
	
	// Check if Manual.yyyy.Q[1-4].csv exist or not
	url = '/API/sourcefile/?file_name=' + source_file;
	var source_file_id;
	$.ajax(
			{	type: "GET", 
				async: false, 
				url: url, 
				success: function(objs) {
					if (objs.length == 0)
						source_file_id = null;
					else
						source_file_id = objs[0].id;
				},
			}
	);
	
	// If Manual.yyyy.Q[1-4].csv not exist. Create!
	if (! source_file_id) {
		url = 'http://edwinmac.local:8000/ozio/add_manual_csv/' + source_file + '/'
		$.ajax(
				{	type: "GET", 
					async: false, 
					url: url, 
					success: function(objs) {
					},
					error: function(objs) {
						alert(objs);
					},
				}
		);
 		return false;
	}
	
	url = '/API/transaction/'
	$.ajax(
			{	type: "POST", 
				async: false, 
				url: url, 
				data: {"date":date, "amount":amount, "info":info, "original_info": original_info, "source_file": source_file_id},
				success: function(objs) {
					on_AddTran_Click_Cancel();
					$("#ozio_home_add_tran_message").css("display", "block");
					$("#ozio_home_add_tran_message_text").text("Transaction added!");
				},
				error: function(objs) {
					$("#add_transaction_message").empty();
					
					var response = "";
					for (k in objs.responseJSON)
						response += k + ":" + objs.responseJSON[k] + '<br>'
					
					$("#add_transaction_message").append(response);
					$("#add_transaction_message").css("display", "block");
				},
			}
	);
	
}

function on_AddTran_Change_Date(date){
	yyyy = date.split('-')[0];
	mm = date.split('-')[1];
	int_mm = parseInt(mm);
	
	value = 'Manual.' + yyyy + '.Q' + parseInt(int_mm / 3 + 1) + '.csv';
	$('#id_transaction-source_file').val(value);
}

function on_AddTran_Change_Info() {
	if ($('#id_info-keyword :selected').text() == new_keyword_option_text)
		$('#add_tran_info_preview').text($('#id_transaction-info').val());
	else
		$('#add_tran_info_preview').text(' ' + $('#id_info-keyword :selected').text() + ': ' + $('#id_transaction-info').val());
}

$(document).ready( function() {
	// Set date input to today
	var now = new Date();
	var yyyy = now.getFullYear();
	var mm = now.getMonth()+1;
	var dd = now.getDate();
	
    if(mm<10){mm='0'+mm} 
    if(dd<10){dd='0'+dd} 
    
    var today = yyyy + '-' + mm + '-' + dd;
    $('#id_transaction-date').val(today);
    on_AddTran_Change_Date($('#id_transaction-date').val())
});