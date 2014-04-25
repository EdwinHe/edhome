///////////////////////////////////////////////////////////
//RUN THESE CODE ONLY WHEN IT IS ON TRANSACTION PAGE
///////////////////////////////////////////////////////////
if ( $('#id_div_page_ozio_transaction').length == 1 ) {
	// Build Outstanding Tab
	buildTableHead_caller('transaction', '#id_thead_outstanding_tran');
	refreshTableContent_caller('/API/transaction/?keyword=', 'transaction', '#id_tbody_outstanding_tran');
	/*hide_table_columns(	'#id_thead_outstanding_tran',
						'#id_tbody_outstanding_tran', 
						json_tran_exclude_cols['#id_thead_outstanding_tran']
	);*/
	
	// Build Span Tab
	buildTableHead_caller('transaction', '#id_thead_span_tran');
	refreshTableContent_caller('/API/transaction/?span_status=N', 'transaction', '#id_tbody_span_tran');
	/*hide_table_columns(	'#id_thead_span_tran',
						'#id_tbody_span_tran', 
						json_tran_exclude_cols['#id_thead_span_tran']
	);*/
	
	// Build All Tran Tab
	buildTableHead_caller('transaction', '#id_thead_tran');
	refreshTableContent_caller('/API/transaction/', 'transaction', '#id_tbody_tran');
	/*hide_table_columns(	'#id_thead_tran',
						'#id_tbody_tran', 
						json_tran_exclude_cols['#id_thead_tran']
	);*/
}



