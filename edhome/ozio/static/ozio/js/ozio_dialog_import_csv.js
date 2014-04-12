$(function() {
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
  });

function chooseFile() {
	$("#id_import_csv").click();
}

function fileChosen() {
	var file_name = $('input[id=id_import_csv]').val().split('\\').pop();
	if ( file_name !== '' )
		$("#file_name").text(file_name);
}

function importFile() {
	$("#id_submit_csv").click();
}