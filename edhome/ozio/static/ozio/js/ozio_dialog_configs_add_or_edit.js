function convertFormToJSON(form){
    var array = $(form).serializeArray();
    var json = {};
    
    for (i in array) {
        json[array[i].name] = array[i].value || '';
    }
    return json;
}

function bind_submit_event() {
	var form = $('#id_form_add_or_edit');
	form.submit(function () {
		$.ajax({
			type: form.attr('method'),
		    url: form.attr('action'),
		    data: convertFormToJSON(form),
		    success: function(rendered_form_html) {
		    	if (rendered_form_html == '') {
		    		$('#configs_dialog_add_edit').dialog('close');
		    		refreshTable_caller(form.attr('action').split('/')[3]);
		    		return false;
		    	}
		    		
		    	$('#configs_dialog_add_edit').empty();
				$('#configs_dialog_add_edit').append(rendered_form_html);
				bind_submit_event();
		    }
		 });
		
		return false;
	});
}

function on_AddOrEdit_Click_Submit(obj_name, obj_id){
	alert(obj_name + ':' + obj_id);
	
	$.ajax(
			{	type: "POST", 
				async: false, 
				url: "/ozio/add_or_edit/" + obj_type + "/" + obj_id + "/",
				success: function(rendered_form_html) {
					$('#configs_dialog_add_edit').empty();
					$('#configs_dialog_add_edit').append(rendered_form_html);
					$('#configs_dialog_add_edit').dialog("open");
				},
			}
	);
	
	return false;
}

function on_AddOrEdit_Click_Cancel(){
	$('#configs_dialog_add_edit').dialog("close");
	return false;
}

$( "#configs_dialog_add_edit" ).dialog({
	autoOpen: false,
	title: 'ADD/EDIT',
	dialogClass: 'ed-dialog-flatly',
	width: 'auto',
	height: 'auto',
	modal: true,
	show: {
		duration: 300
	},
});