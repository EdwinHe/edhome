$( "#import_cba_csv_dialog" ).dialog({
	autoOpen: false,
	title: 'IMPORT CSV',
	dialogClass: 'ed-dialog-flatly',
	width: 'auto',
	modal: true,
	show: {
		duration: 300
	},
});

$( "#import_cba_csv" ).click(function() {
	$( "#import_cba_csv_dialog" ).dialog( "open" );
});

function chooseFile() {
	$("#id_import_csv").click();
}

function fileChosen() {
	var chosen_files = document.getElementById('id_import_csv').files;
	
	var list_of_file = "";
	list_of_file += '<div class="alert alert-dismissable alert-success">';
	for (var x = 0; x < chosen_files.length; x++) {
		list_of_file += chosen_files[x].name + '<br>'; 
	}
	list_of_file += '</div>';
	
	$("#file_name").empty();
	$("#file_name").append(list_of_file);
	
	/*
	var file_name = $('input[id=id_import_csv]').val().split('\\').pop();
	if ( file_name !== '' )
		$("#file_name").text(file_name);
	*/
}

function importFile() {
	$("#id_submit_csv").click();
}