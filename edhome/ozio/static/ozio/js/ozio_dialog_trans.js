$( "#transactions_dialog" ).dialog({
	autoOpen: false,
	title: 'TRANSACTIONS',
	dialogClass: 'ed-dialog-flatly',
	width: '90%',
	height: 600,
	modal: true,
	show: {
		duration: 300
	},
});

$( "#transactions" ).click(function() {
	$( "#transactions_dialog" ).dialog( "open" );
});
